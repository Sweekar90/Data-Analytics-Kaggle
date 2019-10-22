# import csv
import json
import os

from utils import getItemDetails

if __name__ == '__main__':
    # code for opening of file
    # input the relative path of the place where you store the json files
    file_path = r'C:\\Users\\srevann\\Desktop\\json_files\\'
    json_files = os.listdir(file_path)
    result = []

    for json_file in json_files:
        print(json_file)

        with open(file_path + json_file) as fp:
            json_array = json.load(fp)

            for elements in json_array:
                # code for data extracting
                item_details = getItemDetails(elements)
                print(type(item_details))

                data_json = {"id":item_details.item_id,
                             "competition": item_details.competition,
                             "author": item_details.name_author,
                             "date_time": item_details.datentime,
                             "overview": item_details.overview,
                             "comments": item_details.comments,
                             "votes": item_details.votes}

                result.append(data_json)

        with open("data_merge.json", "w") as json_elements:
            json.dump(result, json_elements)

