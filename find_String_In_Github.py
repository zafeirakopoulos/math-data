import pybase64
import requests
import json

def find_String_In_Github(str):
    r_repo = requests.get('https://api.github.com/repos/yilmazedis/newRepository/contents/',
                 headers={'Authorization': 'access_token b678440c02e85ae287d3ec8ececedf4f4c208920'})
    list = []
    for i in range(len(r_repo.json())):
        repo_name = json.loads(json.dumps(r_repo.json()[i]))["name"]
        if repo_name == ".gitignore":
            continue
        print(repo_name)

        r_name = requests.get('https://api.github.com/repos/yilmazedis/newRepository/contents/' + repo_name,
                         headers={'Authorization': 'access_token b678440c02e85ae287d3ec8ececedf4f4c208920'})

        resp_dict = json.loads(json.dumps(r_name.json()))

        resp_string = pybase64.standard_b64decode(resp_dict["content"]).decode("utf-8")

        if resp_string.find(str) != -1:
            list.append([[repo_name],[resp_dict["sha"]]])

    return list

list = find_String_In_Github("units")
print(*list,sep='\n')
