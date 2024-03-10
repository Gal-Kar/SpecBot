import json
import platform
from urllib.parse import urlparse
import sys

def find_all_domain_links(soup, url) -> set:
    domain_name = urlparse(url).netloc
    path = urlparse(url).path
    formatted_links = []
    links = {link.get('href') for link in soup.find_all('a', href=True)}

    for link in links:
        if not is_domain_link(link, domain_name): continue
        if link in ["/", "#"]: continue
        if link.startswith("#"): continue

        if link.startswith("/"):
            formatted_links.append(link)
        elif link.startswith("?"): # php format
            formatted_links.append(path + link)
        else:
            formatted_links.append("/" + link)
    return set(formatted_links)

def is_domain_link(link, domain):
    if link == None: return False

    is_full_url = 'www.' in link or 'http' in link
    if is_full_url and link not in domain:
        return False
    return True

def find_all_forms_with_methods(soup):
    forms = soup.find_all('form')
    forms_list = []

    for form in forms:
        form_dict = {}
        method = form.get('method')
        action = form.get('action')

        if not method: method = "GET"
        if not action: action = "/"

        form_dict['method'] = method.upper()
        form_dict['action'] = action

        form_inputs = form.find_all('input')
        if len(form_inputs) > 0:
            form_dict['inputs'] = {}

        for inner_input in form_inputs:
            name = inner_input.get('name')
            input_type = inner_input.get('type')

            if name:
                form_dict['inputs'][name] = input_type

        forms_list.append(form_dict)

    return forms_list

def write_to_json(filename, data):
    with open(filename, "w") as outfile:
        json.dump(data, outfile)

    outfile.close()

def read_json_file(filename) -> dict:
    with open(filename, 'r') as file:
        data = json.load(file)

    return data

def signal_handler(signal, frame):
    print("\nExiting...\n")
    sys.exit(0)

def path_based_on_os(path):
    return path.replace("/", "\\") if platform.system() == 'Windows' else path.replace("\\", "/")