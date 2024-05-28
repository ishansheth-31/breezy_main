from openai import OpenAI
from pymongo import MongoClient
import os
import re
import logging
import assemblyai as aai
from prompts import MAIN_PROMPT, DOCUMENTATION_PROMPT
from utils import parse_report_sections
from bson import ObjectId

facility_id = '66561810cf408ac02573b706'
new_patient_id = '665623dd0cc7f4b6b3919022'

# Initialize OpenAI and MongoDB clients
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

aai.settings.api_key = "f47fc69f44914e5d973f9d2f719ba271"

mongoClient = MongoClient('mongodb+srv://ishansheth31:Kevi5han1234@breezytest1.saw2kxe.mongodb.net/')
db = mongoClient["BreezyPatient"]
patients_collection = db["patient"]
conversations_collection = db["conversation"]
reports_collection = db["report"]

class MedicalChatbot:

    def __init__(self):
        self.context = [{"role": "system", "content": MAIN_PROMPT}]
        self.finished = False
        self.patient_info = {
            'Subjective': '',
            'Objective': '',
            'Analysis': '',
            'Plan': '',
            'Implementation': '',
            'Evaluation': ''
        }
        self.initial_questions_answers = ""
        self.patient_id = new_patient_id
        self.conversation_json = []

    def handle_initial_questions(self, initial_questions_dict):
        self.initial_questions_dict = initial_questions_dict
        last_answer = initial_questions_dict.get("Finally, what are you in for today?", "")

        try:
            patient_data = {
                "height": self.initial_questions_dict.get("What is your approximate height?", ""),
                "weight": self.initial_questions_dict.get("What is your approximate weight?", ""),
                "medications": self.initial_questions_dict.get("Are you currently taking any medications?", ""),
                "recent_surgeries": self.initial_questions_dict.get("Have you had any recent surgeries?", ""),
                "drug_allergies": self.initial_questions_dict.get("Do you have any known drug allergies?", ""),
                "visit_reason": self.initial_questions_dict.get("Finally, what are you in for today?", ""),
            }
            patients_collection.update_one(
                {"_id": ObjectId(self.patient_id)},
                {"$set": patient_data},
            )

            patients_collection.update_one(
                {"_id": ObjectId(self.patient_id)},
                {"$set": {"status" : "complete"}},
            )


        except Exception as e:
            print(f"Error updating patient data: {e}")

        return last_answer


    def should_stop(self, message):
        if "we'll see you in the office later today" in message.lower():
            self.finished = True

    def generate_response(self, message):
        self.context.append({'role': 'user', 'content': message})
        self.conversation_json.append({'role': 'user', 'content': message})
        response = client.chat.completions.create(
            model="gpt-4",
            messages=self.context
        )
        assistant_message = response.choices[0].message.content
        self.context.append({'role': 'assistant', 'content': assistant_message})
        self.conversation_json.append({'role': 'assistant', 'content': assistant_message})

        return assistant_message

    def create_report(self):
        chat_history = self.get_full_conversation()[1:]
        new_prompt = DOCUMENTATION_PROMPT

        chat_history_string = ""
        for message in chat_history:
            role = message['role'].capitalize()
            content = message['content'].replace('\n', ' ')  # Replace newlines with spaces
            chat_history_string += f"{role}: {content}\n"

        new_prompt += chat_history_string

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": new_prompt}]
            )
            return response
        except Exception as e:
            logging.error(f"Error generating report: {e}")
            return ""

    def get_full_conversation(self):
        """
        Return the full conversation history.
        """
        return self.context

    def extract_and_save_report(self, report_content):
        """
        Extract the report content from the response and save it as a JSON document,
        including initial questions and answers at the top.
        """
        try:
            # Parse the generated report text to get the SOAP sections
            report_sections = parse_report_sections(report_content)

            # Save report to MongoDB
            report_data = {
                "patient_id": self.patient_id,
                "subjective": report_sections.get('Subjective', ''),
                "objective": report_sections.get('Objective', ''),
                "analysis": report_sections.get('Analysis', ''),
                "plan": report_sections.get('Plan', ''),
                "implementation": report_sections.get('Implementation', ''),
                "evaluation": report_sections.get('Evaluation', '')
            }
            reports_collection.insert_one(report_data)
            logging.info(f"Report data inserted for patient ID: {self.patient_id}")

            # Save conversation to MongoDB
            conversation_data = {
                "patient_id": self.patient_id,
                "conversation_json": self.conversation_json
            }
            conversations_collection.insert_one(conversation_data)
            logging.info(f"Conversation data inserted for patient ID: {self.patient_id}")

            # Return the JSON report data
            return report_data
        except Exception as e:
            logging.error(f"Error extracting and saving report: {e}")
            return f"An error occurred: {str(e)}"
