from django.contrib import admin
from member.models import UserProfile
from member.models import Friendship
from lobbys.models import Lobby
from lobbys.models import PlayersLobby
from lobbys.models import Invitation

admin.site.register(UserProfile)
admin.site.register(Friendship)
admin.site.register(Lobby)
admin.site.register(PlayersLobby)
admin.site.register(Invitation)