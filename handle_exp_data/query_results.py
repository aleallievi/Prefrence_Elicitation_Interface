import pickle
import cv2

with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/exp2_results/woi_questions.data', 'rb') as f:
    questions = pickle.load(f)
with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/exp2_results/woi_answers.data', 'rb') as f:
    answers = pickle.load(f)


def query(t_quad, t_pt, t_answer="all"):
    for i in range(len(questions)):
        assignment_qs = questions[i]
        assignment_as = answers[i]
        sample_n = assignment_as[0]
        with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/exp2_data_samples/sample' + str(sample_n) + "/sample"+ str(sample_n) + "_dict.pkl", 'rb') as f:
            sample_dict = pickle.load(f)
        for q,a in zip(assignment_qs, assignment_as):
            if q == "sampleNumber":
                continue


            num = int(q.replace("query",""))
            point = sample_dict.get(num)
            quad = point.get("quadrant")
            pt = point.get("name").split("_")[0]

            if quad == t_quad and pt == t_pt and (t_answer == "all" or a == t_answer):
                #show image
                path = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/all_formatted_imgs/dsdt_formatted_imgs/"
                path += pt + "/" + point.get("name")
                img = cv2.imread(path)
                cv2.imshow("queried",img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

query("dsdt","(0, -2.0)")
