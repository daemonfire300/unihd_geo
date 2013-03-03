import logging
logger = logging.getLogger(__name__)

from django.db import models


"""
    A lobby starts a game.
"""
STATES = {
              "notstartedyet" : 0,
              "running" : 1,
              "paused" : 2,
              "complete" : 3
              }

class Game(models.Model):
    state = models.SmallIntegerField(default=STATES["notstartedyet"])
    
    def pause(self):
        logger.info("Attempting to pause game (Lobby: %s, Owner: %s)" % (self.lobby, self.lobby.owner))
        if self.state is STATES["running"]:
            self.state = STATES["paused"]
            self.save()
            logger.info("Game successfully paused")
        else:
            logger.warning("Game is already paused or in a state where it can not be paused. Current state %s" % self.state)
    
    def __unicode__(self):
        return self.state