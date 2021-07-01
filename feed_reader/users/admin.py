from django.contrib import admin

from users.models import Forum, Collection, Post, Filter, Profile

admin.site.register(Forum)
admin.site.register(Collection)
admin.site.register(Post)
admin.site.register(Filter)
admin.site.register(Profile)