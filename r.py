from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# SAVING TO CURRENT DIRECTORY
file_path = "waste_management_research_framework.pdf"

styles = getSampleStyleSheet()
content = []

content.append(Paragraph("Research Framework: Household Waste Management and Collection Barriers", styles['Title']))
content.append(Spacer(1,20))

sections = {
"1. Research Title": """
Assessment of Household Waste Management Practices and Barriers in Urban Waste Collection Systems.
""",

"2. Research Objectives": """
• Understand household waste management practices including segregation and disposal behavior.
• Examine awareness of waste management regulations among residents.
• Identify operational challenges faced by waste collectors and waste pickers.
• Analyze the role of recycling businesses in the waste management supply chain.
• Investigate root causes of unauthorized waste disposal in public places.
• Identify gaps in waste collection infrastructure and services.
""",

"3. Research Questions": """
• What are the current household waste management practices?
• How aware are residents of local waste management rules?
• What operational challenges do waste collectors and waste pickers face?
• What challenges do recycling businesses encounter in obtaining recyclable waste?
• What are the reasons for improper waste disposal in public areas?
• To what extent are residents’ waste disposal needs met by current systems?
""",

"4. Research Hypotheses": """
H1: Higher awareness of waste segregation rules leads to better household waste management practices.
H2: Lack of waste collection infrastructure increases unauthorized waste disposal.
H3: Proper household waste segregation improves efficiency of waste collectors.
H4: Economic incentives influence participation of waste pickers in recycling activities.
""",

"5. Conceptual Framework": """
Awareness of Waste Rules → Household Waste Segregation Behavior → Efficiency of Waste Collection → Recycling and Disposal Outcomes.
External factors include infrastructure availability, government policies, economic incentives, and social attitudes.
""",

"6. Sampling Strategy": """
Target groups:
Residents – Understand household waste practices
Waste Pickers – Identify ground-level collection challenges
Waste Collectors – Understand operational issues
Waste Businesses – Understand recycling supply chain

Suggested sample sizes:
Residents: 100–200
Waste Pickers: 20–30
Waste Collectors: 20–30
Waste Businesses: 10–15
""",

"7. Data Analysis Plan": """
Quantitative Analysis:
• Frequency distribution
• Percentage analysis
• Cross-tabulation
• Correlation analysis

Qualitative Analysis:
• Thematic analysis
• Coding responses into categories
• Identifying common operational challenges
""",

"8. Expected Outcomes": """
• Identification of gaps in household waste segregation practices.
• Understanding operational challenges faced by waste collectors and pickers.
• Insights into recycling supply chain barriers.
• Evidence of infrastructure or policy gaps affecting waste management.
""",

"9. Possible Recommendations": """
• Awareness campaigns for waste segregation.
• Improved waste collection infrastructure.
• Support programs for waste pickers.
• Incentives for recycling businesses.
• Stronger enforcement of waste management policies.
"""
}

for section, text in sections.items():
    content.append(Paragraph(section, styles['Heading2']))
    content.append(Spacer(1,8))
    for line in text.strip().split("\n"):
        content.append(Paragraph(line, styles['BodyText']))
        content.append(Spacer(1,4))
    content.append(Spacer(1,12))

doc = SimpleDocTemplate(file_path, pagesize=A4)
doc.build(content)

print(f"Success! PDF generated at: {file_path}")