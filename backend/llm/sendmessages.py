from twilio.rest import Client
from pymongo import MongoClient
from bson import ObjectId

facility_id = '665103d70423a23be7bd49f4'
patient_id = '6654f5b67b54fa78e33c3af6'

mongoClient = MongoClient('mongodb+srv://ishansheth31:Kevi5han1234@breezytest1.saw2kxe.mongodb.net/')
db = mongoClient["BreezyPatient"]
patients_collection = db["patient"]
facilities_collection = db["facilities"]

def string_builder(patient_name, practice_name, link):
    final_string = f"""Good Evening {patient_name}!

We are excited to have you at {practice_name} tomorrow morning for your appointment. Please complete the Breezy Medical Assessment below so we have your pre-visit information on file.

{link}

Have a great rest of your night!
"""
    return final_string

def parse_databases(facility_id):
    global patient_id
    patient_entry = patients_collection.find_one({"_id": ObjectId(patient_id)})
    facility_entry = facilities_collection.find_one({"_id": ObjectId(facility_id)})
    patient_name = patient_entry.get("firstName", "N/A")
    phone_number = patient_entry.get('contact', [{}])[0].get('phone', 'Phone number not found')
    practice_name = facility_entry.get("name", "N/A")
    return phone_number, patient_name, practice_name

def main():
    client = Client(twilio_account_sid, twilio_auth_token)
    link = 'http://localhost:3000/' + str(patient_id)

    phone_number, patient_name, practice_name = parse_databases(facility_id=facility_id)
    final_string = string_builder(patient_name=patient_name, practice_name=practice_name, link=link)

    try:
        message = client.messages.create(
            from_=twilio_sender_phone_number,
            body=final_string,
            to=phone_number
        )
        
        response_data = {
            "message_sid": message.sid,
            "status": message.status,
            "date_sent": message.date_sent,
        }

        patients_collection.update_one({"_id": ObjectId(patient_id)}, {"$set": {"status": "sent"}})

        return response_data
    except Exception as e:
        print("Message couldn't send:", str(e))
        return "Message couldn't send"

if __name__ == "__main__":
    main()
