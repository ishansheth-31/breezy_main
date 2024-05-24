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

# example patient id: 664fa2bcecd2141c88ddbb62
"""
Mapping (SOAP note section to FHIR resource):

Subjective - Observation
Objective - Observation

Analysis - Condition

Plan - CarePlan

Implementation - Procedure for clinical intervations (surgery, therapy), MedicationRequest for prescribed medication

Evaluation - Observation to document follow-up findings, Condition to note changes in the patient's health status
"""

def fetch_patient_reports(patient_id):
    try:
        patient_reports = reports_collection.find({"patient_id": ObjectId(patient_id)})
        reports_list = list(patient_reports)
        reports_json = json.dumps(reports_list, default=str, indent=4)
                
        return reports_json
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

