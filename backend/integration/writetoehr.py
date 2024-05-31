from pymongo import MongoClient
from bson import ObjectId
import json
import os
import re
import logging
import requests

mongoClient = MongoClient('mongodb+srv://ishansheth31:Kevi5han1234@breezytest1.saw2kxe.mongodb.net/')
db = mongoClient["BreezyPatient"]
patients_collection = db["patient"]
conversations_collection = db["conversation"]
reports_collection = db["report"]

api_key = "V1pKNlItaFB3c29kRk9XTGVlQkNyOjRmYzdjNTIwLWY4N2EtNGUyOS1iYzQ2LWJiYjIwNWJlZmZhYQ"

patient_id = '018fac9b-7117-7a64-8119-846b6650a282'
url = f'https://api.sandbox.metriport.com/medical/v1/patient/{patient_id}/consolidated'

def fetch_patient_reports(patient_id):
    try:
        patient_reports = reports_collection.find({"metriport_patient_id": patient_id})
        reports_list = list(patient_reports)
        reports_json = json.dumps(reports_list, default=str, indent=4)
                
        return reports_json
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

report = fetch_patient_reports(patient_id=patient_id)
data = json.loads(report)
subjective_value = data[0]['subjective']
objective_value = data[0]['objective']
analysis_value = data[0]['analysis']
plan_value = data[0]['plan']
implementation_value = data[0]['implementation']
evaluation_value = data[0]['evaluation']

data = {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": [
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "category": [{
                    "coding": [{
                        "system": "http://hl7.org/fhir/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }]
                }],
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "8302-2",
                        "display": "Body Height"
                    }]
                },
                "valueQuantity": {
                    "value": 168,
                    "unit": "cm",
                    "system": "http://unitsofmeasure.org",
                    "code": "cm"
                }
            }
        }
    ]
}



"""
Mapping (SOAP note section to FHIR resource):

Subjective - Observation
Objective - Observation

Analysis - Condition

Plan - CarePlan

Implementation - Procedure for clinical intervations (surgery, therapy), MedicationRequest for prescribed medication

Evaluation - Observation to document follow-up findings, Condition to note changes in the patient's health status
"""

# - medications/dosage/how often per day/in what way
# - subjective information --> rest of soap note
#     - timeframe
#     - severity
#     - symptoms
#     - body site
# - impementation/evaluation
# - height
# - weight
# - condition summary - chief complaint
# - past surgeries
# - drug allergies
# - lifestyle - smoking