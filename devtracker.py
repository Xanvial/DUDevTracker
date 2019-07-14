import praw

# Create the Reddit instance and log in
reddit = praw.Reddit('bot1')

ULreddit = reddit.subreddit("underlords")

print("vian test")
#print(reddit.user.me())
for comment in ULreddit.comments(limit=1000):
    #print(comment.author.name)
    if(comment.author.name == "Xanvial"):
        print("----")
        print(comment.submission.title)
        print(comment.body)
        print(comment.permalink)

print("vian test done")
