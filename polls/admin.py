from polls.models import Poll
from polls.models import Choice
from member.models import UserProfile
from member.models import Friendship
from game.models import Game
from lobbys.models import Lobby

from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('visualized_relation', 'accepted')

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(UserProfile)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Game)
admin.site.register(Lobby)