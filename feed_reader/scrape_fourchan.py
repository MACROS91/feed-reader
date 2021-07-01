import os
import sys
import django 
import datetime

sys.path.append(r'C:\Users\RMacD\OneDrive\Desktop\feed-reader\feed_reader')
os.environ["DJANGO_SETTINGS_MODULE"] = "feed_reader.settings"
django.setup()

from users.models import Post, Forum

import basc_py4chan

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
    get_threads()