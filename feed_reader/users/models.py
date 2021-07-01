from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# https://stackoverflow.com/questions/51853161/django-while-displaying-list-of-articles-show-favourite-status-of-each-articles

# General purpose model to hold 
class Forum(models.Model):
    site = models.CharField(
        max_length=100,
        choices=[
            ('Reddit', 'Reddit'),
            ('4Chan', '4Chan')
        ]
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Collection(models.Model):
    # Collections hold a standard set of subreddits
    # and/or fourchan boards related to a specific topic
    name = models.CharField(max_length=200)
    description = models.TextField()
    forum_subscriptions = models.ManyToManyField(Forum, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE,null=True)
    url = models.URLField()
    post = models.TextField()
    post_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title[:50]

class Filter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    watching = models.BooleanField(default=False)
    hiding = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user','post')

# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# Create profile for user to store subscriptions, etc.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collections = models.ManyToManyField(Collection)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@ receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()