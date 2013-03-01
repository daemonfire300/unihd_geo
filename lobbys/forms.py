from django import forms
from lobbys.models import Lobby
from lobbys.models import PlayersLobby

class LobbyCreationForm(forms.ModelForm):
    title = forms.CharField(min_length=5, max_length=50)
    description = forms.CharField(widget=forms.Textarea, max_length=230)
    max_players = forms.ChoiceField(choices=tuple((x,x) for x in range(1,20)))
    
    class Meta:
        model = Lobby
        fields = ("title", "description", "max_players")
    
    def __init__(self, request=None, *args, **kwargs):
        super(LobbyCreationForm, self).__init__(*args, **kwargs)
        self.request = request
        
    def clean(self):
        cleaned_data = super(LobbyCreationForm, self).clean()
        if Lobby.objects.filter(owner=self.request.user.userprofile).count():
            raise forms.ValidationError(u'You already have a running lobby.')
        return cleaned_data 
    
    def save(self, commit=True):
        lobby = super(LobbyCreationForm, self).save(commit=False)
        lobby.owner = self.request.user.userprofile
        lobby.open_game(commit=False)
        if commit:
            lobby.save()
            assoc = PlayersLobby(lobby=lobby, player=lobby.owner)
            assoc.save()
        return lobby