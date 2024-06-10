import requests
from twilio.rest import Client
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_key = os.getenv('MONGO_KEY')
mongoClient = MongoClient(mongo_key)
db = mongoClient["BreezyPatient"]
patients_collection = db["patient"]
facilities_collection = db["facilities"]

url = "https://api.sandbox.metriport.com/medical/v1/patient"

querystring = {"facilityId":"018fac77-0184-7d50-b179-2da1a34bd1dd"}

payload = {
    "firstName": "Ishan",
    "lastName": "Sheth",
    "dob": "2004-01-01",
    "genderAtBirth": "M",
    "personalIdentifiers": [],
    "contact": [
        {
            "phone": "+14049155010",
            "email": "kevishan@gmail.com"
        }
    ],
    "externalId": "123456789",
    "address": [
        {
            "addressLine1": "708 Spring St.",
            "city": "Baltimore",
            "state": "MD",
            "zip": "30327",
            "country": "USA"
        }
    ]
}
headers = {
    "x-api-key": "V1pKNlItaFB3c29kRk9XTGVlQkNyOjRmYzdjNTIwLWY4N2EtNGUyOS1iYzQ2LWJiYjIwNWJlZmZhYQ",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
reports_json = response.json()

inserted_id = patients_collection.insert_one(reports_json).inserted_id
patients_collection.update_one({"_id": inserted_id}, {"$set": {"status": "not sent"}})

