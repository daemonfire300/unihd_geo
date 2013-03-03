from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    playername = models.CharField(max_length=100)
    playerclass = models.CharField(max_length=64)
    friends = models.ManyToManyField("self", through='Friendship', related_name='friendship', symmetrical=False)
    games_player = models.IntegerField(default=0)
    experience = models.BigIntegerField(default=0)
    
    def get_lobby(self):
        try:
            lobbies = self.lobbies.all()
            lobby = lobbies[0]
            return lobby
        except IndexError:
            return False
    def is_owner(self, lobby=None):
        if lobby is not None:
            if lobby.owner.id == self.id:
                return True
            else:
                return False
        else:
            return False
        
    def get_friendship(self):
        return Friendship.objects.filter(own_profile=self)
    
    def get_friendship_requests(self):
        return Friendship.objects.filter(friend_profile=self, accepted=False)
        
    def __unicode__(self):
        return self.playername + " (%s)" % self.user.username


class Friendship(models.Model):
    own_profile = models.ForeignKey(UserProfile, related_name="me")
    friend_profile = models.ForeignKey(UserProfile, related_name="friend")
    accepted = models.BooleanField(default=False)
    
    def visualized_relation(self):
        return "%s &#8594; %s" % (self.own_profile.playername, self.friend_profile.playername)
    visualized_relation.allow_tags = True
    
    def __unicode__(self):
        return self.friend_profile.playername