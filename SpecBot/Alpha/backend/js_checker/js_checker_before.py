import raw_data_helper as rd
import js_checker_helper as check_function
import os
import json

# TODO: get raw data file
# raw_data = argv[0]
raw_data = os.path.join('resources','raw-data.json')
reduced_data = rd.create_url_content_dict(raw_data)

#search keywords dictionary
with open(os.path.join('resources','replace_keywords.json'), 'r') as f:
    replace_keywords = json.load(f)

#result dictionary
result = {}

# go over each url
for url in reduced_data:
    result[url] = {}
    result[url]["priority"] = "low"
    result[url]["type"] = "Syntax Error"
    result[url]["lastLine"] = -1
    result[url]["lastColumn"] = -1
    result[url]["firstColumn"] = -1
    result[url]["message"] = ""
    result[url]["suggestions"] = []
    #go over each content block:
    for block in reduced_data[url]:
        result[url]["block_code"] = {}
        result[url]["block_code"][block] = []
        counter = 0
        for word in block.split(' '):
            if word in replace_keywords:
                function_to_call = getattr(check_function, replace_keywords[word])
                output = function_to_call(block,counter)
                if(output):
                    result[url]["block_code"][block].append(output)
            counter += 1
        if len(result[url]["block_code"][block]) == 0:
            del result[url]["block_code"]

rd.write_dict_to_file(result,"js_checker_result.json")