import praw
import os
import psycopg2

def bot_login():
	# Create the Reddit instance and log in
	reddit = praw.Reddit(username = os.environ["reddit_username"],
						 password = os.environ["reddit_password"],
						 client_id = os.environ["client_id"],
						 client_secret = os.environ["client_secret"],
						 user_agent = "Xanvial")
	return reddit

def mainloop(reddit, latest_comment_utc):
	ULreddit = reddit.subreddit("underlords")
	TrackerReddit = reddit.subreddit("UnderlordsDevTracker")

	userlist = [
		"Xanvial"
		]

	for u in userlist:
		print("user:"+u)

	print("vian test")
	#print(reddit.user.me())
	TimeLastCheckComment=float(latest_comment_utc)
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
	return str(tmpTime)

if __name__ == "__main__":
	while True:
		try:
			print ("\nFetching comments..")
			r = bot_login()
			latest_utc = os.environ["latest_comment_utc"]
			print ("start utc:"+latest_utc)
			while True:
				# Fetching all new comments that were created after created_utc time
				print ("\nstart utc from env:"+os.environ["latest_comment_utc"])
				latest_utc = mainloop(r, latest_utc)
				print ("\nlatest_utc:"+latest_utc)
				os.environ["latest_comment_utc"] = latest_utc
				time.sleep(1*60) # sleep 1 minutes

		except Exception as e:
			print (str(e.__class__.__name__) + ": " + str(e))
			time.sleep(15)
