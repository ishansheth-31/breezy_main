import re

def parse_report_sections(report_text):
    patterns = {
        "Chief Complaint (CC)": r"Chief Complaint \(CC\):\s*(.*?)\n(?=History of Present Illness \(HPI\):)",
        "History of Present Illness (HPI)": r"History of Present Illness \(HPI\):\s*(.*?)\n(?=Medical history:)",
        "Medical history": r"Medical history:\s*(.*?)\n(?=Surgical history:)",
        "Surgical history": r"Surgical history:\s*(.*?)\n(?=Family history:)",
        "Family history": r"Family history:\s*(.*?)\n(?=Social History:)",
        "Social History": r"Social History:\s*(.*?)\n(?=Review of Systems \(ROS\):)",
        "Review of Systems (ROS)": r"Review of Systems \(ROS\):\s*(.*?)\n(?=Current Medications:)",
        "Current Medications": r"Current Medications:\s*(.*?)\n(?=Objective:)",
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