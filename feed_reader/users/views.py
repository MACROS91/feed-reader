from django.shortcuts import render, redirect 

from django.views.generic import ListView

from users.models import Forum, Collection, Profile, \
                         Post, Filter

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        forum = self.kwargs['forum']
        print(forum) 
        if forum == None:
            return Post.objects.all()
        else:
            return Post.objects.filter(forum__name=forum)

class CollectionListView(ListView):
    model = Post

    def get_queryset(self):
        collection = self.kwargs['collection']
        if collection == None:
            return Post.objects.all()
        else:
            # Get a list of forum_ids associated with collection and filter posts to match
            # Will the same subreddit in multiple collections result in duplicates?
            forum_ids = Collection.objects.filter(name=collection).values_list('forum_subscriptions')
            forums = Forum.objects.filter(id__in=forum_ids)
            forum_list = [forum.name for forum in forums]
            return Post.objects.filter(forum__name__in=forum_list)

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['collections'] = Collection.objects.all()
        return context

def reject_from_collection():
    pass

def add_to_collection_watchlist():
    pass