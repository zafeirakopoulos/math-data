import pybase64
import requests
import json

url_api = 'https://api.github.com/repos/yilmazedis/newRepository/contents/'
access_token = 'access_token b678440c02e85ae287d3ec8ececedf4f4c208920'

def find_string_in_github(str):

    r_repo = requests.get(url_api, headers={'Authorization': access_token})
    list = []
    for i in range(len(r_repo.json())):
        repo_name = json.loads(json.dumps(r_repo.json()[i]))["name"]
        if repo_name == ".gitignore":
            continue
        print(repo_name)

        r_name = requests.get(url_api + repo_name,headers={'Authorization': access_token})

        resp_dict = json.loads(json.dumps(r_name.json()))

        resp_string = pybase64.standard_b64decode(resp_dict["content"]).decode("utf-8")

        if resp_string.find(str) != -1:
            list.append([[repo_name], [resp_dict["sha"]]])

    return list


list = find_string_in_github("units")

print(*list,sep='\n')