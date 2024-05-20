import re

def parse_report_sections(report_text):
    patterns = {
        "Subjective": r"Subjective:\s*(.*?)\n(?=Objective:)",
        "Objective": r"Objective:\s*(.*?)\n(?=Analysis:)",
        "Analysis": r"Analysis:\s*(.*?)\n(?=Plan:)",
        "Plan": r"Plan:\s*(.*?)\n(?=Implementation:)",
        "Implementation": r"Implementation:\s*(.*?)\n(?=Evaluation:)",
        "Evaluation": r"Evaluation:\s*(.*)"
    }
    sections = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, report_text, re.DOTALL)
        if match:
            sections[key] = match.group(1).strip()
    return sections
