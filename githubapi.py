from flask import Flask
from flask_restful import Api, Resource
import requests
import re
import getpass

valid_github_username = "^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$"

app = Flask("GithubFollowerTree")
api = Api(app)

class gitUser(Resource) :
	def get(self, username) :
		if (re.match(valid_github_username, username)) :
			req = requests.get("https://api.github.com/users/" + username, auth=(AppUser, AppPass)).json()
			resultJSON = getMoreFollowers(username, depth=3, length=5)
			return resultJSON, 200
			
		else :
			return "Username not valid", 400

def getMoreFollowers(username, depth=-1, length=5) :
	# recursively call to get followers at each branch
	if depth == -1 :
		return []
	req = requests.get("https://api.github.com/users/" + username + "/followers", auth=(AppUser, AppPass))
	json = req.json()
	results = [username]
	for iter1 in range(0, min(len(json), length)) :
		follower = getMoreFollowers(json[iter1]["login"], depth - 1)
		if follower != [] :
			results.append(follower)

	return results

#input user authentication to bypass the 60 requests per hour limitation
AppUser = getpass.getpass(prompt="Enter app username: ")
AppPass = getpass.getpass(prompt="Enter app password: ")

api.add_resource(gitUser, "/<string:username>")
app.run()