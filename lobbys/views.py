# import the logging library
import logging
from django.http.response import HttpResponse
from django.utils import simplejson

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from lobbys.forms import LobbyCreationForm
from lobbys.models import Lobby
from lobbys.models import PlayersLobby

@login_required(login_url='/member/login/')
def create(request):
    #userprofile = request.user.userprofile
    if request.method == 'POST':
        form = LobbyCreationForm(data=request.POST, request=request)
        if form.is_valid():
            lobby = form.save()
            logger.info("Created a new lobby: %s" % lobby)
            return HttpResponseRedirect("/lobby/%s" % lobby.id)
    else:
        form = LobbyCreationForm()
    return render(request, 'lobbys/create.html', {"form": form})

@login_required(login_url='/member/login/')
def show(request, lobby_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    user = request.user.userprofile
    is_owner = user.is_owner(lobby=lobby)
    return render(request, 'lobbys/show.html', {"lobby": lobby, "user": user, "is_owner": is_owner})

@login_required(login_url='/member/login/')
def listplayers(request, lobby_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    return HttpResponse(simplejson.dumps(lobby.players.all()), 'application/json')

@login_required(login_url='/member/login/')
def join(request, lobby_id):
    if request.method == 'POST':
        lobby = get_object_or_404(Lobby, id=lobby_id)
        user = request.user.userprofile
        if lobby.max_players > lobby.players.count():
            if user.get_lobby() is False:
                assoc = PlayersLobby(lobby=lobby, player=user)
                assoc.save()
                return render(request, 'lobbys/show.html', {"lobby": lobby, "user": user})
            elif user.get_lobby().id == lobby.id:
                return render(request, 'lobbys/show.html', {"lobby": lobby, "user": user})
            else:
                return HttpResponseRedirect("/member/profile/")
        else:
            return render(request, 'lobbys/show.html', {"lobby": lobby, "full": True})