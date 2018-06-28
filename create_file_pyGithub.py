from github import Github

new_repo = "newRepository"
g = Github("access_token")
user = g.get_user()

repo = g.get_user().get_repo(new_repo)
print(repo)

## İlk argümanda dosyanın tam yolu belirtilmeli
## Commit belirtilmedi
## 3. parametre ise dosyanın içeriği
file = repo.create_file("/path.txt", "initial commit", "içerik\n2. satır")
print(file)