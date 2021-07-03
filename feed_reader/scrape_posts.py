import os
import sys
import django 
import datetime
import tqdm
import basc_py4chan

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

def get_threads(board='biz'):
    
    b = basc_py4chan.Board(board)
    threads = b.get_all_threads()

    forum = Forum.objects.filter(name=board).first()

    for thread in threads:
        print(thread.topic)
        id = thread.posts[0].post_id
        title = thread.topic
        url = thread.posts[0].url
        text = thread.posts[0].text_comment
        post_date = datetime.datetime.now()
        print(post_date)
        num_comments = len(thread.posts)

        closed = thread.closed
        archived = thread.archived

        fourchan_obj, _ = Post.objects.update_or_create(id=id)
        fourchan_obj.id = id
        fourchan_obj.forum = forum
        fourchan_obj.title = title
        fourchan_obj.url = url
        fourchan_obj.post = text 
        fourchan_obj.post_date = post_date

        fourchan_obj.save()

        print(f'{id}')

if __name__ == '__main__':
    forums = Forum.objects.all()
    for subreddit in tqdm.tqdm(forums.filter(site='Reddit')):
        get_posts(subreddit.name)
    for board in tqdm.tqdm(forums.filter(site='4Chan')):
        get_threads(board.name)
