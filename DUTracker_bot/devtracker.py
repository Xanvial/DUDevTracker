import praw
import time
import os


def bot_login():
	# Create the Reddit instance and log in
	reddit = praw.Reddit(username = os.environ["reddit_username"],
						 password = os.environ["reddit_password"],
						 client_id = os.environ["client_id"],
						 client_secret = os.environ["client_secret"],
						 user_agent = "Xanvial")
	return reddit

def mainloop(reddit, TimeLastCheckComment):
	ULreddit = reddit.subreddit("underlords")
	TrackerReddit = reddit.subreddit("UnderlordsDevTracker")

	userlist = [
		"Xanvial"
		]

	for u in userlist:
		print("user:"+u)

	print("vian test")
	#print(reddit.user.me())
	tmpTime = 0
	for comment in ULreddit.comments(limit=1000):
		if (tmpTime == 0):
			tmpTime = comment.created_utc   # save the latest comment time
		if(comment.created_utc > TimeLastCheckComment and comment.author.name in userlist):
			print("----")
			print(comment.submission.title)
			print(comment.body)
			print(comment.permalink)
			print(comment.created_utc)
			#TrackerReddit.submit(comment.submission.title+" ["+comment.author.name+"]", url="https://www.reddit.com"+comment.permalink)

	print(tmpTime)
	print("vian test done")
	return tmpTime

if __name__ == "__main__":
	while True:
		try:
			print ("\nFetching comments..")
			r = bot_login()
			created_utc = 0
			while True:
				# Fetching all new comments that were created after created_utc time
				created_utc = mainloop(r, created_utc)
				time.sleep(5*60) # sleep 5 minutes

		except Exception as e:
			print (str(e.__class__.__name__) + ": " + str(e))
			time.sleep(15)
