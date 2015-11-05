import praw
import time
import loginCredentials as cred # this only exists locally, you need to make your own

class AyyBot():
	def __init__(self):
		global r # because there can only be one instance of this alive 
		r=praw.Reddit(user_agent="AyyBot0.1 by /u/brianchenito ")
		r.set_oauth_app_info(cred.redditId,cred.redditSecret,cred.redirectUri)
		self.refreshToken()
		self.authenticatedUser=r.get_me()

	def refreshToken(self): 
		r.refresh_access_information(cred.redditRefresh)

	def checkSubmissions(self,subReddit): #searches front page for keywords via recurseComments(), launching point for other funcs
		currentSub=r.get_subreddit("testingground4bots")
		for submission in currentSub.get_hot(limit=5):
			print("\nTitle: {0} ".format( submission.title))
			self.recurseComments(submission.comments)  

	def recurseComments(self,comments):	#digs through comment trees for "Ayy"
		for comment in comments:
				print("Comment: {0}".format(comment.body))
				if "ayy" in str(comment.body).lower():	
					if self.lmaoCheck(comment.replies):
						print("Okay to comment")
						comment.reply(self.lmaoGenerate(comment.body))
						time.sleep(600)
					else: 
						print("Not Okay to comment")
				self.recurseComments(comment.replies)

	def lmaoCheck(self,comments): #checks if a comment containing "Lmao is already present"
		for comment in comments:
			if  "lmao" in str(comment.body):
				return False
		return True

	def lmaoGenerate(self, ayy):
		startIndex=ayy.lower().index("ayy")
		if ayy[startIndex].isupper():
			if ayy[startIndex+1].isupper():
				lmaoList=["LMA"]
			else:
				lmaoList=["Lma"]
		else:
			lmaoList=["lma"]	

		for i in range(0,ayy.lower().count("y")-1):
			if ayy[startIndex+1+i].isupper():
				lmaoList.append("o".upper())
			else:
				lmaoList.append("o")
		return "".join(lmaoList)

if __name__ == "__main__":
		bot=AyyBot()

		while True:
			print("Active Bot: {0}".format(bot.authenticatedUser))
			bot.checkSubmissions("testingground4bots")
			bot.refreshToken()
			time.sleep(600)
