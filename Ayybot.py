from __future__ import print_function
import sys
import praw
import time
import loginCredentials as cred # this only exists locally, you need to make your own
import approvedSubs

def safeprint(safe): # to help handle weird unicode stuff, its not gonna render right but it wont throw errors
	try:
		print(safe)
	except UnicodeEncodeError:
		if sys.version_info >= (3,):
			print(safe.encode('utf8').decode(sys.stdout.encoding))
		else:
			print(safe.encode('utf8'))

class AyyBot():
	def __init__(self):
		global r # because there can only be one instance of this alive 
		r=praw.Reddit(user_agent="AyyBot0.1 by /u/brianchenito ")
		r.set_oauth_app_info(cred.redditId,cred.redditSecret,cred.redirectUri)
		self.refreshToken()
		self.authenticatedUser=r.get_me()

	def refreshToken(self): 
		r.refresh_access_information(cred.redditRefresh)

	def checkComments(self,subReddit): #searches front page for keywords via recurseComments(), launching point for other funcs
		currentSub=r.get_subreddit(subReddit)
		currentComments=currentSub.get_comments(limit=5000)
		self.recurseComments(currentComments)


	def recurseComments(self,comments):
		for comment in comments:
			print(".", end="")
			if "ayy" in str(comment.body).lower(): 
				safeprint("\nComment: {0} ".format(comment.body))
				if self.ayyCheck(comment.body)[2]!=0:
					startIndex=self.ayyCheck(comment.body)[1]
					endIndex=self.ayyCheck(comment.body)[2] #optimize later
					if self.lmaoCheck(comment):
						print("\n okay to comment\n")
						comment.reply(self.lmaoGenerate(comment.body,startIndex,endIndex))
						time.sleep(300)
						

	def ayyCheck(self,ayy):# checks validity of comment syntax, also outputs start and end of the ayy
		lowAyy=ayy.lower()
		startIndex=lowAyy.index("ayy")
		for i in range(lowAyy.index("ayy"), lowAyy.index("a"),-1 ):
			if lowAyy[i-1]!="a":
				startIndex=i
				break
			if i==(lowAyy.index("a")+1):
				startIndex=lowAyy.index("a")
		endIndex=startIndex
		if len(ayy.split())>1:
			print("Ayy fail, multiword\n")
			return (ayy,0,0)
		for i in range(startIndex, len(ayy)-1):
			if lowAyy[i]=="a":
				endIndex+=1
				if lowAyy[i+1] !="a" and lowAyy[i+1]!="y":
					print("Ayy fail, syntax error(a)")
					return (ayy,0,0)
			elif lowAyy[i]=="y":
				if lowAyy[i+1]=="y":
					endIndex+=1
				if lowAyy[i+1]!="y" and lowAyy[i+1].isalpha():
					print("Ayy fail, syntax error(y)")
					return(ayy,0,0)
		if startIndex!=0:
			if ayy[startIndex-1].lower()=="g":
				print("ayy fail, edge case (G)")
				return(ayy,0,0)# special edge case exception
			if ayy[startIndex-1].lower()=="h":
				print("ayy fail, edge case (H)")
				return(ayy,0,0)# special edge case exception
			if ayy[startIndex-1].lower()=="y":
				print("ayy fail, edge case (Y)")
				return(ayy,0,0)# special edge case exception				
		return(ayy,startIndex,endIndex)

	def lmaoCheck(self,comment): #checks if a comment containing "Lmao is already present"
		commentsCheck= comment.replies
		try:
			if  "lmao" in str(comment.body).lower():
				print("found lmao already in comments")
				return False
			for comment in commentsCheck:
				if  "lmao" in str(comment.body).lower():
					print("found lmao already in comments")
					return False	
				if str(comment.author)=="Ayy_Bot":
					return False
			print("no reply 'Lmao' found")
			return True
		except AttributeError:
			print(" hit moreComments()")# it turns out things start getting weird with extremely deep trees, unsafe to return true
			return False

	def lmaoGenerate(self, ayy, startIndex,endIndex): #builds lmao comment
		lmaoList=[]
		for i in range(0, startIndex):
			lmaoList.append(ayy[i])
		if ayy[startIndex].isupper():
			if ayy[startIndex+1].isupper():
				lmaoList.append("LMA")
			else:
				lmaoList.append("Lma")
		else:
			lmaoList.append("lma")
		for i in range(startIndex+1,endIndex):
			if ayy[i].lower()=="a":
				if ayy[i].isupper():
					lmaoList.append("a".upper())
				else:
					lmaoList.append("a")
			else:
				if ayy[i].isupper():
					lmaoList.append("o".upper())
				else:
					lmaoList.append("o")
		for i in range(endIndex+1, len(ayy)):
			lmaoList.append(ayy[i])
		generatedLmao=''.join(lmaoList)
		safeprint("commenting:\n{0}" .format(generatedLmao))
		return generatedLmao

if __name__ == "__main__":
		bot=AyyBot()

		while True:
			try: # sometimes the api times out, or the servers go down
				print("Active Bot: {0}".format(bot.authenticatedUser))
				bot.checkComments(approvedSubs.approved)
				bot.refreshToken()
				print("\nrefreshing search")
			except Exception as e:
				print("\nError {0}".format(str(e)))
				time.sleep(300)
				pass
			