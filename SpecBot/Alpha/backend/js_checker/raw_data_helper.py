import json
import re
import os

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def keep_only_scripts(url_content_dict):
    new_dict = {}
    pattern = re.compile(r'<script>(.*?)</script>', re.DOTALL)
    for url,content in url_content_dict.items():
        new_dict[url] = pattern.findall(content)
    return new_dict

def print_dict(url_content_dict):
    for key,val in url_content_dict.items():
        print("--------------------------------------------------------------------------")
        print(key)
        for i in val:
            print("~~~~~~~~~~~~~~")
            print(i)

def write_dict_to_file(url_content_dict,file_name):
    with open(os.path.join('resources',file_name), "w") as outfile:
        json.dump(url_content_dict, outfile, indent=4)

def create_url_content_dict(raw_data_file):
    # file=read_json_file(raw_data_file)
    url_content_dict = {}
    for url in raw_data_file:
        for title in raw_data_file[url]:
            if title == "content":
                url_content_dict[url]=raw_data_file[url][title]

    return keep_only_scripts(url_content_dict)








