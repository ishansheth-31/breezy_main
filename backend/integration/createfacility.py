from pymongo import MongoClient
from bson import ObjectId
import json
import os
import re
import logging
import requests

mongoClient = MongoClient('mongodb+srv://ishansheth31:Kevi5han1234@breezytest1.saw2kxe.mongodb.net/')
db = mongoClient["BreezyPatient"]
facilities_collection = db["facilities"]

headers = {
    "Content-Type": "application/json",
    "x-api-key": "V1pKNlItaFB3c29kRk9XTGVlQkNyOjRmYzdjNTIwLWY4N2EtNGUyOS1iYzQ2LWJiYjIwNWJlZmZhYQ",
}

data = {
    "name": "Breezy Medical",
    "npi": "1234567893",
    "tin": "12-3456789",
    "active": True,
    "address": {
        "addressLine1": "3050 M.L.K. Dr",
        "addressLine2": "suite M",
        "city": "Atlanta",
        "state": "GA",
        "zip": "30311",
        "country": "USA",
    },
}

url = "https://api.sandbox.metriport.com/medical/v1/facility"

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("Facility created successfully.")
    print(response.json()) 
else:
    print(f"Failed to create facility. Status code: {response.status_code}")
    print(response.text)  

reports_json = response.json()
facilities_collection.insert_one(reports_json)
