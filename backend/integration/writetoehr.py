from pymongo import MongoClient
from bson import ObjectId
import json
import os
import re
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

mongo_key = os.getenv('MONGO_KEY')
mongoClient = MongoClient(mongo_key)
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
        "category": [
          {
            "coding": [
              {
                "system": "http://hl7.org/fhir/observation-category",
                "code": "symptom",
                "display": "Symptom"
              }
            ]
          }
        ],
        "code": {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "29857009",
              "display": "Chest pain"
            }
          ]
        },
        "subject": {
          "reference": "Patient/665623dd0cc7f4b6b3919022"
        },
        "valueString": "Severe chest pain, sharp and burning, exacerbates with deep breathing and movement, rated 8 on a scale of 1-10."
      }
    },
    {
      "resource": {
        "resourceType": "Condition",
        "clinicalStatus": {
          "coding": [
            {
              "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
              "code": "active",
              "display": "Active"
            }
          ]
        },
        "code": {
          "coding": [
            {
              "system": "http://snomed.info/sct",
              "code": "46635009",
              "display": "Chest pain (finding)"
            }
          ]
        },
        "subject": {
          "reference": "Patient/665623dd0cc7f4b6b3919022"
        },
        "note": [
          {
            "text": "Patient reports severe chest pain for the last four days, rated as 8 on a scale of 1-10. No radiation of pain to other parts of the body."
          }
        ]
      }
    },
    {
      "resource": {
        "resourceType": "Patient",
        "id": "665623dd0cc7f4b6b3919022",
        "extension": [
          {
            "url": "http://hl7.org/fhir/StructureDefinition/patient-ethnicity",
            "valueCodeableConcept": {
              "coding": [
                {
                  "system": "urn:oid:2.16.840.1.113883.6.238",
                  "code": "2135-2",
                  "display": "Hispanic or Latino"
                }
              ]
            }
          }
        ],
        "gender": "male",
        "birthDate": "1984-03-12"
      }
    },
    {
    "resource": {
        "resourceType": "MedicationStatement",
        "medicationCodeableConcept": {
        "coding": [
            {
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
            "code": "860975",
            "display": "Aspirin 81 MG Oral Tablet"
            }
        ]
        },
        "subject": {
        "reference": "Patient/665623dd0cc7f4b6b3919022"
        },
        "status": "active",
        "effectiveDateTime": "2023-01-01",
        "taken": "yes",
        "reasonCode": [
        {
            "text": "Preventive treatment"
        }
        ]
        }
    },
    {
    "resource": {
        "resourceType": "FamilyMemberHistory",
        "patient": {
        "reference": "Patient/665623dd0cc7f4b6b3919022"
        },
        "status": "completed",
        "relationship": {
        "coding": [
            {
            "system": "http://hl7.org/fhir/v3/RoleCode",
            "code": "FTH",
            "display": "father"
            }
        ]
        },
        "condition": [
        {
            "code": {
            "coding": [
                {
                "system": "http://hl7.org/fhir/sid/icd-10",
                "code": "I25.10",
                "display": "Chronic ischemic heart disease, unspecified"
                }
            ]
            },
            "outcome": "deceased"
        }
        ]
    }
    },
    {
    "resource": {
        "resourceType": "Observation",
        "subject": {
        "reference": "Patient/665623dd0cc7f4b6b3919022"
        },
        "status": "final",
        "category": [
        {
            "coding": [
            {
                "system": "http://hl7.org/fhir/observation-category",
                "code": "social-history",
                "display": "Social History"
            }
            ]
        }
        ],
        "code": {
        "coding": [
            {
            "system": "http://loinc.org",
            "code": "75275-8",
            "display": "Tobacco smoking status NHIS"
            }
        ],
        "text": "Patient reports no tobacco use"
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