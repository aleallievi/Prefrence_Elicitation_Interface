import boto3
import xmltodict
import json
import pickle
from datetime import datetime

# with open('results.pickle', 'rb') as temp:
#     results = pickle.load(temp)
#
aws_access_key_id =
aws_secret_access_key = 

create_hits_in_production = True #use Sandbox for testing and production for actually giving workers jobs
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
# # response = client.update_expiration_for_hit(HITId=hit_id,ExpireAt=datetime(2015, 1, 1))
# assignments = client.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted'])
# if assignments['NumResults'] > 0:
#     for assign in assignments['Assignments']:
#         client.approve_assignment(AssignmentId=assign['AssignmentId'])
#
# # try:
# client.delete_hit(HITId=hit_id)

# client.delete_hit(HITId=hit_id)
# #
#
hit = client.get_hit(HITId=hit_id)
# Get a list of the Assignments that have been submitted
assignmentsList = client.list_assignments_for_hit(
    HITId=hit_id,
    AssignmentStatuses=['Submitted', 'Approved'],
    MaxResults=100
)
assignments = assignmentsList['Assignments']
# item['assignments_submitted_count'] = len(assignments)
questions = []
answers = []

woi = ["AJD65G9H2QUE9","A34D413HR7ZIFM","A1IFIK8J49WBER","A2WPKP73S4MBLK","A272X64FOZFYLB","A3G5IPGLH1IIZN","A4T4577P6JL6R","A1F9KLZGHE9DTA","A24LB89P1BPKKF","A26K8OELA8ZDI9","A7P3R1AIA4TVV","A1AKL5YH9NLD2V","A3FGT6EU39C6S4"]


for assignment in assignments:

    # Retreive the attributes for each Assignment
    worker_id = assignment['WorkerId']
    assignment_id = assignment['AssignmentId']
    # reward = assignment['Reward']

    # client.send_bonus(WorkerId=worker_id,AssignmentId=assignment_id,BonusAmount= "5",Reason= "Thanks for completing the hIT!")

    # Retrieve the value submitted by the Worker from the XML
    answer_dict = xmltodict.parse(assignment['Answer'])
    answer = answer_dict['QuestionFormAnswers']['Answer']
    # answers.append(answer)
    # print (answer)
    # print ("\n")
    if worker_id in woi:
        assignment_questions = []
        assignment_answers = []
        for a in answer:
            question = a.get("QuestionIdentifier")
            answer = a.get("FreeText")
            assignment_questions.append(question)
            assignment_answers.append(answer)
        questions.append(assignment_questions)
        answers.append(assignment_answers)
    # Approve the Assignment (if it hasn't been already)
    if assignment['AssignmentStatus'] == 'Submitted':
        client.approve_assignment(
            AssignmentId=assignment_id,
            OverrideRejection=False
        )
with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/exp2_results/woi_questions.data', 'wb') as f:
    pickle.dump(questions, f)
with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/exp2_results/woi_answers.data', 'wb') as f:
    pickle.dump(answers, f)
#
# print (answers)





# print (answers)
# # Add the answers that have been retrieved for this item
# # item['answers'] = answers
#
#
# # hit = client.get_hit(HITId="3D1UCPY6HLSQHEHE46SLUPDZ4F783D")
# #3HL3WX654HG4Z7L863H242MOLZRQPH
# #3HL3WX654HG4Z7L863H242MOLZRQPH
# #3HL3WX654HG4Z7L863H242MOLZRQPH
# #
# #
# # for item in results:
# #     # Get the status of the HIT
# #     hit = client.get_hit(HITId=item['hit_id'])
# #     item['status'] = hit['HIT']['HITStatus']
# #     # Get a list of the Assignments that have been submitted
# #     assignmentsList = client.list_assignments_for_hit(
# #         HITId="item['hit_id']",
# #         AssignmentStatuses=['Submitted', 'Approved'],
# #         MaxResults=10
# #     )
# #     assignments = assignmentsList['Assignments']
# #     item['assignments_submitted_count'] = len(assignments)
# #     answers = []
# #     for assignment in assignments:
# #
# #         # Retreive the attributes for each Assignment
# #         worker_id = assignment['WorkerId']
# #         assignment_id = assignment['AssignmentId']
# #
# #         # Retrieve the value submitted by the Worker from the XML
# #         answer_dict = xmltodict.parse(assignment['Answer'])
# #         answer = answer_dict['QuestionFormAnswers']['Answer']
# #         answers.append(answer)
# #
# #         # Approve the Assignment (if it hasn't been already)
# #         if assignment['AssignmentStatus'] == 'Submitted':
# #             client.approve_assignment(
# #                 AssignmentId=assignment_id,
# #                 OverrideRejection=False
# #             )
# #
# #     # Add the answers that have been retrieved for this item
# #     item['answers'] = answers
# #
# # print(json.dumps(results,indent=2))
