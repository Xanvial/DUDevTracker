import praw

# Create the Reddit instance and log in
reddit = praw.Reddit('bot1')

ULreddit = reddit.subreddit("underlords")
TrackerReddit = reddit.subreddit("UnderlordsDevTracker")

print("vian test")
#print(reddit.user.me())
for comment in ULreddit.comments(limit=1000):
    if(comment.author.name == "Xanvial"):
        print("----")
        print(comment.submission.title)
        print(comment.body)
        print(comment.permalink)
        TrackerReddit.submit(comment.submission.title+" ["+comment.author.name+"]", url="https://www.reddit.com"+comment.permalink)

print("vian test done")
