import praw
import os
import psycopg2
import time
from userlist import usernames

def bot_login():
	# Create the Reddit instance and log in
	reddit = praw.Reddit(username = os.environ["reddit_username"],
						 password = os.environ["reddit_password"],
						 client_id = os.environ["client_id"],
						 client_secret = os.environ["client_secret"],
						 user_agent = "Xanvial")
	return reddit

def mainloop(source, target, latest_comment_utc):
	TimeLastCheckComment=float(latest_comment_utc)
	tmpTime = 0
	for comment in source.comments(limit=1000):
		if (tmpTime == 0):
			tmpTime = comment.created_utc   # save the latest comment time
		if(comment.created_utc > TimeLastCheckComment and comment.author.name in userlist.usernames):
			print("-- Found --")
			print(comment.submission.title)
			print(comment.comment.author.name)
			print(comment.body)
			print(comment.permalink)
			print(comment.created_utc)
			target.submit(comment.submission.title+" ["+comment.author.name+"]", url="https://www.reddit.com"+comment.permalink+"?context=1")

	return str(tmpTime)

if __name__ == "__main__":
	while True:
		try:
			DATABASE_URL = os.environ['DATABASE_URL']
			conn = psycopg2.connect(DATABASE_URL, sslmode='require')
			cur = conn.cursor()
			cur.execute("SELECT latest_utc from data")
			latest_utc = cur.fetchall()

			if (len(latest_utc) > 0):
				latest_utc = str(latest_utc[0][0])
			else:
				latest_utc = "0"
			 
			print("Dev List:")
			for u in userlist.usernames:
				print("  "+u)
				
			print ("\nFetching comments..")
			r = bot_login()
			print ("start utc:"+latest_utc)
			
			ULreddit = r.subreddit("underlords")
			TrackerReddit = r.subreddit("UnderlordsDevTracker")
			
			while True:
				# Fetching all new comments that were created after latest_utc time
				print ("\nstart utc from db:"+latest_utc)
				latest_utc = mainloop(ULreddit, TrackerReddit, latest_utc)
				print ("\nlatest_utc:"+latest_utc)
				cur.execute("UPDATE data SET latest_utc = {}". format(latest_utc))
				conn.commit()
				time.sleep(1*60) # sleep 1 minutes

		except Exception as e:
			print (str(e.__class__.__name__) + ": " + str(e))
			time.sleep(15)
