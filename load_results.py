import boto3
import xmltodict
import json
import pickle

with open('results.pickle', 'rb') as temp:
    results = pickle.load(temp)

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

for item in results:
    # Get the status of the HIT
    hit = client.get_hit(HITId=item['hit_id'])
    item['status'] = hit['HIT']['HITStatus']
    # Get a list of the Assignments that have been submitted
    assignmentsList = client.list_assignments_for_hit(
        HITId=item['hit_id'],
        AssignmentStatuses=['Submitted', 'Approved'],
        MaxResults=10
    )
    assignments = assignmentsList['Assignments']
    item['assignments_submitted_count'] = len(assignments)
    answers = []
    for assignment in assignments:

        # Retreive the attributes for each Assignment
        worker_id = assignment['WorkerId']
        assignment_id = assignment['AssignmentId']

        # Retrieve the value submitted by the Worker from the XML
        answer_dict = xmltodict.parse(assignment['Answer'])
        answer = answer_dict['QuestionFormAnswers']['Answer']
        answers.append(answer)

        # Approve the Assignment (if it hasn't been already)
        if assignment['AssignmentStatus'] == 'Submitted':
            client.approve_assignment(
                AssignmentId=assignment_id,
                OverrideRejection=False
            )

    # Add the answers that have been retrieved for this item
    item['answers'] = answers

print(json.dumps(results,indent=2))
