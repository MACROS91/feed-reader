import os
import sys
import django 
import datetime

import praw

sys.path.append(r'C:\Users\RMacD\OneDrive\Desktop\feed-reader\feed_reader')
os.environ["DJANGO_SETTINGS_MODULE"] = "feed_reader.settings"
django.setup()

from users.models import Post, Forum

reddit = praw.Reddit(
    client_id="d1J2EBZQ4MAI6Q",
    client_secret="zFcGC4BFxiqoH4vleKI_YMMdrIz12A",
    user_agent="crypto browser"
)

def get_posts(subreddit):
    forum = Forum.objects.filter(name=subreddit).first()
    print(forum)
    for submission in reddit.subreddit(subreddit).new():
        id = submission.id
        title = submission.title
        url = submission.url
        selftext = submission.selftext
        post_date = datetime.datetime.now()

        num_comments = 0

        reddit_obj, _ = Post.objects.update_or_create(id=id)
        reddit_obj.id = id
        reddit_obj.title = title
        reddit_obj.forum = forum
        reddit_obj.url = url
        reddit_obj.post = selftext 
        reddit_obj.post_date = post_date

        reddit_obj.save()

if __name__ == '__main__':
    get_posts('cryptomoonshots')