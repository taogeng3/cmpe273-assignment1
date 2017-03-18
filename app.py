from flask import Flask
from github import Github
import yaml
import json
import sys
import re

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Dockerized Flask App!!"

@app.route("/v1/<filename>")
def get_config(filename):
    github_url = sys.argv[1]
    pat = re.compile(r'^https://github.com/(.*)/(.*)$')
    pat_search = pat.search(github_url)
    if not pat_search:
      return "GitHub url error!"
    user = pat_search.group(1)
    repo_name = pat_search.group(2)

    g = Github()
    repo = g.get_user(user).get_repo(repo_name)
    try:
      f = repo.get_contents(filename)
      return f.decoded_content
    except:
      if not filename.endswith(".json"): 
          return "The " + filename + " file does not exist in GitHub!"

    yml_filename = filename.replace(".json", ".yml")
    try:
      yml_f = repo.get_contents(yml_filename)
      return json.dumps(yaml.load(yml_f.decoded_content))
    except:
      return "The yml file for " + filename + " does not exist in GitHub!"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
