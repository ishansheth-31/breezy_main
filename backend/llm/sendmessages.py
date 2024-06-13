from twilio.rest import Client
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_sender_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

mongo_key = os.getenv('MONGO_KEY')
mongoClient = MongoClient(mongo_key)
db = mongoClient["southernurogyno"]
patients_collection = db["patient"]

def string_builder(patient_name, date, time, link):
    final_string = f"""Good Evening {patient_name}!

We are excited to have you at Southern Urogynocology on {date} at {time} for your appointment. Please complete the Breezy Medical Assessment below so we have your pre-visit information on file.

{link}

We look forward to seeing you!
"""
    return final_string

def send_message(phone_number, patient_name, date, time, link):
    client = Client(twilio_account_sid, twilio_auth_token)
    final_string = string_builder(patient_name=patient_name, date=date, time=time, link=link)
    try:
        message = client.messages.create(
            from_=twilio_sender_phone_number,
            body=final_string,
            to=phone_number
        )
        return {
            "message_sid": message.sid,
            "status": message.status,
            "date_sent": message.date_sent,
        }
    except Exception as e:
        print("Message couldn't send:", str(e))
        return "Message couldn't send"

def add_patients_and_send_messages(csv_path):
    patients_df = pd.read_csv(csv_path, delimiter=',')

    for _, row in patients_df.iterrows():
        patient_data = {
            "firstName": row['fName'],
            "lastName": row['lName'],
            "contact": [{"phone": row['Phone']}],
            "appointment": {
                "date": row['Appt_Date'],
                "time": row['Appt_Time']
            },
            "newPatient": row['New_Patient'],
        }

        result = patients_collection.insert_one(patient_data)
        patient_id = result.inserted_id
        link = f'https://breezy-main-1bre.vercel.app/{patient_id}'  # Append the token to the link
        send_message(row['Phone'], row['fName'], row['Appt_Date'], row['Appt_Time'], link)

def main():
    csv_path = 'backend\llm\patients.csv'  # Updated path to the CSV file
    add_patients_and_send_messages(csv_path)

if __name__ == "__main__":
    main()
