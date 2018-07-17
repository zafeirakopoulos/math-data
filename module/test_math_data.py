from math_data import math_data


data = math_data()

r = {
    "datatype": "polinom",
    "index": "something...",
    "raw": "something...",
    "features": "something...",
    "semantics": "something...",
    "context":  {"edge": {"1": 1, "2": 2},
                 "vertex": [{"first": 2, "second": 1},
                            {"first": 23, "second": 55}]},
    "typeset": "something...",
    "commit": "something..."
}

#firstly add some file after and store its index sha, And you can remove after that
#response = data.add_instance(r)
#print(response)



r = {
    "datatype": "polinom",
    "sha": "1b729f1219072705f1209820af80d525d60c3f42"
}

response = data.remove_instance(r)
print(response)

r = {
    "datatype": "graph",
    "sha": "e2b6af3d97a7f55cf9bd1b54a70614ca7598b04d",
    "index": "deneme",
    "raw": "something...",
    "features": "something...",
    "semantics": "something...",
    "context":  {"edge": {"1": 33, "2": 5555},
                 "vertex": [{"first": 4, "second": 4},
                            {"first": 3, "second": 55}]},
    "typeset": "something...",
    "commit": "update_repo"
}

#response = data.update_instance(r)
#print(response)

r = {
    "datatype": "graph",
    "sha": "5ac30052d1a800b2d03bf8b841366b1652f470ee",

}

#response = data.retrieve_instance(r)
#print(response)

'''
import git
repo = git.Repo('/Users/yilmaz/PycharmProjects/miniserver/templates/graph/index')
commits = repo.iter_commits()
#commits.reverse()

print(commits.hexsha)
print(commits.message)
print(commits.stats.total)
print(commits.stats.files)
'''