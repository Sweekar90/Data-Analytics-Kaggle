import json
import requests
import time

data_list = []

# range should be iterated for every 1000 requests starting from 1 to 75000. Now the there can be more than 75000 requests as well.
for i in range(45000, 46000):
    # sending requests to kaggle
    data = requests.get("https://www.kaggle.com/topics/" + str(i) + ".json")
    print(str(i) + ":" + str(data.status_code))
    time.sleep(0.5)
    if data.status_code == 200:
        try:
            # collect data
            json_data = data.json()
        except ValueError:
            print("Wrong status code for topic: " + str(i))
        else:
            data_list.append(json_data)

with open("C:\\Users\\srevann\\Desktop\\json_files\\46000.json", 'w') as outfile:
    json.dump(data_list, outfile)