import boto3
import xmltodict
import json
import pickle

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
)


QUESTION_XML = open("interface.xml", "r")
question_xml = QUESTION_XML.read()

# question_xml = QUESTION_XML.format(html_layout)

TaskAttributes = {
    'MaxAssignments': 100,
    # How long the task will be available on MTurk (24 hours)
    'LifetimeInSeconds': 60*60*24,
    # How long Workers have to complete each item (10 minutes)
    'AssignmentDurationInSeconds': 60*10,
    # The reward you will offer Workers for each response
    'Reward': '0.00',
    'Title': 'Choose the best image',
    'Keywords': 'trajectory',
    'Description': 'Choose which image is better'
}

results = []
hit_type_id = ''


response = client.create_hit(
    **TaskAttributes,
    Question=question_xml,
)
hit_type_id = response['HIT']['HITTypeId']
results.append({
    'hit_id': response['HIT']['HITId']
})

print("You can view the HITs here:")
print(mturk_environment['preview']+"?groupId={}".format(hit_type_id))
with open('results.pickle', 'wb') as temp:
    pickle.dump(results, temp)
