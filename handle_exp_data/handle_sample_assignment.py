import boto3
import xmltodict
import json
import pickle
from datetime import datetime

# with open('results.pickle', 'rb') as temp:
#     results = pickle.load(temp)
#
aws_access_key_id = "AKIAZPBE4QB4EOCTWGYE"
aws_secret_access_key = "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"

create_hits_in_production = False #use Sandbox for testing and production for actually giving workers jobs
environments = {
  "production": {
    "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
    "preview": "https://www.mturk.com/mturk/preview"
  },
  "sandbox": {
    "endpoint":
          "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
    "preview": "https://workersandbox.mturk.com/mturk/preview"
  },
}
mturk_environment = environments["production"] if create_hits_in_production else environments["sandbox"]

session = boto3.Session(profile_name='stephane.hk')
client = session.client(
    service_name='mturk',
    region_name='us-east-1',
    endpoint_url=mturk_environment['endpoint'],
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
#
hit_id = "3X878VYTJJ1HXCSOEW1HHY61WSD7FJ"

hit = client.get_hit(HITId=hit_id)
# Get a list of the Assignments that have been submitted
assignmentsList = client.list_assignments_for_hit(
    HITId=hit_id,
    AssignmentStatuses=['Submitted', 'Approved'],
    MaxResults=100
)
assignments = assignmentsList['Assignments']

for assignment in assignments:
    # Retreive the attributes for each Assignment
    worker_id = assignment['WorkerId']
    assignment_id = assignment['AssignmentId']
