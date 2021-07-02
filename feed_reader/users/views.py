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
