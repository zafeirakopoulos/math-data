from github import Github

g = Github("b678440c02e85ae287d3ec8ececedf4f4c208920")

for repo in g.get_user().get_repos():
    print(repo.name)