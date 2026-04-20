from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
import os

# Fix for Mac semaphore leaks
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class LocalLLM:
    def __init__(self):
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

        print("Loading LLM (TinyLlama)...")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Apple Silicon optimization
        if torch.backends.mps.is_available():
            self.device = "mps"
            dtype = torch.float16
        else:
            self.device = "cpu"
            dtype = torch.float32

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=dtype,
            device_map=self.device,
            low_cpu_mem_usage=True
        )

        self.model.eval()

    def generate(self, prompt):

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        ).to(self.device)

        # Debug (helps catch prompt overflow)
        print("Prompt tokens:", len(inputs["input_ids"][0]))

        output = self.model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.4,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id
        )

        prompt_length = inputs["input_ids"].shape[-1]
        new_tokens = output[0][prompt_length:]

        text = self.tokenizer.decode(
            new_tokens,
            skip_special_tokens=True
        ).strip()

        if not text:
            return "I couldn't generate a response."

        return text


class DeepResearchAgent:

    def __init__(self, tools):
        self.tools = tools
        self.llm = LocalLLM()

    def run(self, question, history=[]):

        clean_q = question.lower().strip()

        # Quick greeting handler
        if clean_q in ["hi", "hello", "hey"]:
            return "Hello! I'm your RAG Assistant. How can I help you analyze your documents?"

        # -------------------------
        # Format conversation history
        # -------------------------

        history_str = ""

        if history:
            for turn in history[-2:]:

                if isinstance(turn, dict):

                    role = turn.get("role", "")
                    content = turn.get("content", "")

                    if role == "user":
                        history_str += f"<|user|>\n{content}</s>\n"

                    elif role == "assistant":
                        history_str += f"<|assistant|>\n{content}</s>\n"

                elif isinstance(turn, (list, tuple)) and len(turn) == 2:

                    user_msg, assistant_msg = turn

                    history_str += f"<|user|>\n{user_msg}</s>\n"
                    history_str += f"<|assistant|>\n{assistant_msg}</s>\n"

        # -------------------------
        # Detect if retrieval needed
        # -------------------------

        requires_search = any(word in clean_q for word in [
            "what",
            "how",
            "find",
            "explain",
            "summarize",
            "pdf",
            "document",
            "according"
        ])

        context_text = ""

        if requires_search:

            vector_results = self.tools.search_vector(question)
            keyword_results = self.tools.search_keyword(question)

            combined_context = vector_results[:3] + keyword_results[:1]

            # Trim context chunks (prevents token overflow)
            cleaned_context = []

            for c in combined_context:
                if isinstance(c, dict):
                    text = c.get("text", "")
                else:
                    text = str(c)

                cleaned_context.append(text[:500])

            combined_context = cleaned_context
            if combined_context:
                context_text = "Context from documents:\n" + "\n".join(combined_context)

            # Remove HTML artifacts
            context_text = re.sub("<.*?>", "", context_text)

        # -------------------------
        # Build prompt
        # -------------------------

        prompt = "<|system|>\nYou are a smart research assistant. Use the provided document context to answer the question. If the answer is not in the documents, say you don't know.</s>\n"

        prompt += history_str

        if context_text:

            prompt += f"<|user|>\n{context_text}\n\nQuestion: {question}</s>\n<|assistant|>"

        else:

            prompt += f"<|user|>\n{question}</s>\n<|assistant|>"

        # -------------------------
        # Generate answer
        # -------------------------

        answer = self.llm.generate(prompt)

        # Cleanup artifacts
        if "Assistant:" in answer:
            answer = answer.split("Assistant:")[-1].strip()

        if not answer:
            return "I couldn't find enough information in the documents to answer that."

        return answer