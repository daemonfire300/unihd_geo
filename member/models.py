from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    playername = models.CharField(max_length=100)
    playerclass = models.CharField(max_length=64)
    friends = models.ManyToManyField(User, through='Friendship', related_name='friends+')
    
    def __unicode__(self):
        return self.playername + " (%s)" % self.user.username
    
class Friendship(models.Model):
    profile = models.ForeignKey(UserProfile)
    user = models.ForeignKey(User)
    accepted = models.BooleanField(default=False)
    
    def visualized_relation(self):
        return "%s &#8594; %s" % (self.profile.playername, self.user.username)
    visualized_relation.allow_tags = True
    
    def __unicode__(self):
        return self.user.username