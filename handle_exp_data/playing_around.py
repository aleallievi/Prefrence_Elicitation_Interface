import json

dsst_data = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_dsst_chosen.json"
with open(dsst_data, 'r') as j:
    dsst_data = json.loads(j.read())

arr = dsst_data.get(str((3.0, -1.0)))
print (len(arr))
