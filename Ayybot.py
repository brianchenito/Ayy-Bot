from __future__ import print_function
import sys
import praw
import time
import loginCredentials as cred # this only exists locally, you need to make your own
import approvedSubs


def safeprint(s): # to help handle weird unicode stuff, its not gonna render right but it wont throw errors
    try:
        print(s)
    except UnicodeEncodeError:
        if sys.version_info >= (3,):
            print(s.encode('utf8').decode(sys.stdout.encoding))
        else:
            print(s.encode('utf8'))

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
		currentSub=r.get_subreddit(subReddit)
		for submission in currentSub.get_hot(limit=5):
			safeprint("\nTitle: {0} ".format( submission.title))
			self.recurseComments(submission.comments)  

	def recurseComments(self,comments):	#digs through comment trees for "Ayy, checks validity of Ayy"
		for comment in comments:
			try:
				if "ayy" in str(comment.body).lower():
					safeprint("Comment: {0}".format(comment.body))
					if self.ayyCheck(comment.body):
						if self.lmaoCheck(comment):
							safeprint("Okay to comment")
							comment.reply(self.lmaoGenerate(comment.body))
							safeprint ("commented '{0}'.\n".format(self.lmaoGenerate(comment.body)))
							time.sleep(600)
						else: 
							safeprint("Not Okay to comment\n")
				self.recurseComments(comment.replies)
			except AttributeError:
				pass

	def ayyCheck(self,ayy):    #verifies
		startIndex=ayy.lower().index("a")
		if ayy[0].lower()!="a":
			if ayy[startIndex-1].isalpha() != False:
				safeprint("preceding char failure")
				return False
		for i in range ((startIndex), len(ayy)-1):
			if ayy[i].lower()=="a":
				if (ayy[i+1].lower()!= "y") and (ayy[i+1].lower()!="a"):
					safeprint("'A' failure in Ayy")
					return False
			if ayy[i].lower()=="y":
				if (ayy[i+1].lower()!= "y") and (ayy[i+1].isalpha() != False):
					safeprint("'Y' failure in Ayy")
					return False
			if (ayy[i].lower()!="a") and (ayy[i].lower()!="y"):
				safeprint("Valid Ayy")
				return True
		safeprint("Valid Ayy")
		return True

	def lmaoCheck(self,comment): #checks if a comment containing "Lmao is already present"
		if  "lmao" in str(comment.body).lower():
			safeprint("found lmao already in comments")
			return False
		commentsCheck= comment.replies
		for comment in commentsCheck:
			if  "lmao" in str(comment.body).lower():
				safeprint("found lmao already in comments")
				return False
		safeprint("Valid Lmao")
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
			safeprint("Active Bot: {0}".format(bot.authenticatedUser))
			bot.checkSubmissions(approvedSubs.approved)
			bot.refreshToken()
			time.sleep(600)
