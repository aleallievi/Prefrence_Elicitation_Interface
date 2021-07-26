import json
import codecs

q1 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/dsst_ql_passing_spaces.json"
q2 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ssst_ql_passing_spaces.json"
q3 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/sss_ql_passing_spaces.json"
q4 = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ql_passing_spaces.json"


with open(q1, 'r') as j:
    q1 = json.loads(j.read())
with open(q2, 'r') as j:
    q2 = json.loads(j.read())
with open(q3, 'r') as j:
    q3 = json.loads(j.read())
with open(q4, 'r') as j:
    q4 = json.loads(j.read())


ex1_dsst = {}
ex1_ssst = {}
ex1_sss = {}
ex1_dsdt = {}
#points to choose:
#44 pts

#dsst
#(0, 0)
#(0, -1.0)
#(1.0, -1.0)
#(1.0, -2.0)
#(2.0, -1.0)
#(3.0, -1.0)


ex1_dsst["(0.0, 0.0)"] = q1.get("(0.0, 0.0)")
ex1_dsst["(0, -1.0)"] = q1.get("(0, -1.0)")
ex1_dsst["(0, -2.0)"] = q1.get("(0, -2.0)")
ex1_dsst["(0, -3.0)"] = q1.get("(0, -3.0)")
ex1_dsst["(1.0, -1.0)"] = q1.get("(1.0, -1.0)")
ex1_dsst["(2.0, -2.0)"] = q1.get("(2.0, -2.0)")
ex1_dsst["(3.0, -3.0)"] = q1.get("(3.0, -3.0)")
ex1_dsst["(2.0, -1.0)"] = q1.get("(2.0, -1.0)")
ex1_dsst["(1.0, -2.0)"] = q1.get("(1.0, -2.0)")
ex1_dsst["(3.0, -1.0)"] = q1.get("(3.0, -1.0)")


#ssst
#(0, 0)
#(0, -1.0)
#(0, -2.0)
#(0, -3.0)

ex1_ssst["(0.0, 0.0)"] = q2.get("(0.0, 0.0)")
ex1_ssst["(0, -1.0)"] = q2.get("(0, -1.0)")
ex1_ssst["(0, -2.0)"] = q2.get("(0, -2.0)")
ex1_ssst["(0, -3.0)"] = q2.get("(0, -3.0)")


#sss/_
#(0, 0)
#(0, -1.0)
#(0, -2.0)
#(0, -3.0)
#(1.0, -1.0)
#(2.0, -2.0)
#(3.0, -3.0)
#(2.0, -1.0)
#(1.0, -2.0)
#(3.0, -1.0)

#(0, 1.0)
#(0, 3.0)
#(3.0, 0)
#(3.0, 3.0)
#(1.0, -3.0)
#(2.0, -3.0)
#(3.0, -2.0)
ex1_sss["(0.0, 0.0)"] = q3.get("(0.0, 0.0)")
ex1_sss["(0, -1.0)"] = q3.get("(0, -1.0)")
ex1_sss["(0, -2.0)"] = q3.get("(0, -2.0)")
ex1_sss["(0, -3.0)"] = q3.get("(0, -3.0)")
ex1_sss["(2.0, -2.0)"] = q3.get("(2.0, -2.0)")
ex1_sss["(3.0, -3.0)"] = q3.get("(3.0, -3.0)")
ex1_sss["(2.0, -1.0)"] = q3.get("(2.0, -1.0)")
ex1_sss["(1.0, -2.0)"] = q3.get("(1.0, -2.0)")
ex1_sss["(3.0, -1.0)"] = q3.get("(3.0, -1.0)")
ex1_sss["(0, 1.0)"] = q3.get("(0, 1.0)")
ex1_sss["(0, 3.0)"] = q3.get("(0, 3.0)")
ex1_sss["(3.0, 0)"] = q3.get("(3.0, 0)")
ex1_sss["(3.0, 3.0)"] = q3.get("(3.0, 3.0)")
ex1_sss["(2.0, -3.0)"] = q3.get("(2.0, -3.0)")
ex1_sss["(3.0, -2.0)"] = q3.get("(3.0, -2.0)")

ex1_dsdt["(0, -1.0)"] = q4.get("(0, -1.0)")
ex1_dsdt["(0, -2.0)"] = q4.get("(0, -2.0)")
ex1_dsdt["(0, -3.0)"] = q4.get("(0, -3.0)")
ex1_dsdt["(1.0, -1.0)"] = q4.get("(1.0, -1.0)")
ex1_dsdt["(2.0, -2.0)"] = q4.get("(2.0, -2.0)")
ex1_dsdt["(3.0, -3.0)"] = q4.get("(3.0, -3.0)")
ex1_dsdt["(2.0, -1.0)"] = q4.get("(2.0, -1.0)")
ex1_dsdt["(1.0, -2.0)"] = q4.get("(1.0, -2.0)")
ex1_dsdt["(3.0, -1.0)"] = q4.get("(3.0, -1.0)")
ex1_dsdt["(0, 1.0)"] = q4.get("(0, 1.0)")
ex1_dsdt["(0, 3.0)"] = q4.get("(0, 3.0)")
ex1_dsdt["(3.0, 0)"] = q4.get("(3.0, 0)")
ex1_dsdt["(3.0, 3.0)"] = q4.get("(3.0, 3.0)")
ex1_dsdt["(1.0, -3.0)"] = q4.get("(1.0, -3.0)")
ex1_dsdt["(2.0, -3.0)"] = q4.get("(2.0, -3.0)")
ex1_dsdt["(3.0, -2.0)"] = q4.get("(3.0, -2.0)")

# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex1_dsst.json", 'w') as fp:
#     json.dump(ex1_dsst,fp)
with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex1_ssst.json", 'w') as fp:
    json.dump(ex1_ssst,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex1_sss.json", 'w') as fp:
#     json.dump(ex1_sss,fp)
# with open("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/ex1_dsdt.json", 'w') as fp:
#     json.dump(ex1_dsdt,fp)
