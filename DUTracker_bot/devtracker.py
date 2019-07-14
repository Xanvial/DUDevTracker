import praw
import time
import os

# Create the Reddit instance and log in
reddit = praw.Reddit(username = os.environ["reddit_username"],
                     password = os.environ["reddit_password"],
                     client_id = os.environ["client_id"],
                     client_secret = os.environ["client_secret"],
                     user_agent = "Xanvial")

ULreddit = reddit.subreddit("underlords")
TrackerReddit = reddit.subreddit("UnderlordsDevTracker")

userlist = [
    "Xanvial"
    ]

for u in userlist:
    print("user:"+u)

print("vian test")
#print(reddit.user.me())
TimeLastCheckComment = 1563097412.0
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
        TrackerReddit.submit(comment.submission.title+" ["+comment.author.name+"]", url="https://www.reddit.com"+comment.permalink)

TimeLastCheckComment = tmpTime
print(TimeLastCheckComment)
print("vian test done")