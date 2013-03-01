from django.db import models
from game.models import Game
from member.models import UserProfile

STATES = {
              "open" : 1,
              "closed" : 0
              }

class FinishedLobby(models.Model):
    owner = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=250)
    max_players = models.SmallIntegerField(default=5)
    state = models.SmallIntegerField(default=STATES["closed"])
    
    def __unicode__(self):
        return self.title

class Lobby(models.Model):
    owner = models.OneToOneField(UserProfile)
    players = models.ManyToManyField(UserProfile, through='PlayersLobby', related_name='players+')
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=250)
    max_players = models.SmallIntegerField(default=5)
    state = models.SmallIntegerField(default=STATES["open"])
    game = models.OneToOneField(Game)
    
    def finish(self):
        f_lobby = FinishedLobby(owner=self.owner, title=self.title, description=self.description, max_players=self.max_players)
        return f_lobby.save()
    
    def open_game(self, commit=True):
        game = Game(state=0)
        game.save()
        self.game = game
        if commit:
            self.save()
    
    def __unicode__(self):
        return self.title

class PlayersLobby(models.Model):
    player = models.ForeignKey(UserProfile)
    lobby = models.ForeignKey(Lobby)
