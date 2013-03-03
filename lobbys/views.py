# import the logging library
import logging
from django.http.response import HttpResponse
from django.utils import simplejson

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from lobbys.forms import LobbyCreationForm
from lobbys.models import Lobby
from lobbys.models import PlayersLobby
from lobbys.models import Invitation
from member.models import UserProfile
from common.http.jsonresponse import Failure, Success

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
def show_all(request):
    lobbies = Lobby.objects.filter(state=1)
    return render(request, 'lobbys/show_all.html', {"lobbies": lobbies})

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

@login_required(login_url='/member/login/')
def invite(request, lobby_id, user_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    invited_user = get_object_or_404(UserProfile, id=user_id)
    user = request.user.userprofile
    is_owner = user.is_owner(lobby=lobby)
    message = {}
    if is_owner:
        if Invitation.objects.filter(issuer=user, player=invited_user, lobby=lobby).count() < 1:
            invitation = Invitation(issuer=user, player=invited_user, lobby=lobby)
            invitation.save()
            message["text"] = "You sent an invitation to %s for your lobby %s" % (invited_user, lobby)
            return Success(message)
        else:
            message["text"] = "You already sent an invitation to %s" % invited_user
            return Failure(message)
    else:
        message["text"] = "You are not the owner of this lobby, you can not issue invitations to it"
        return Failure(message)

@login_required(login_url='/member/login')
def response_invite(request, lobby_id, action):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    user = request.user.userprofile
    results = Invitation.objects.filter(player=user, lobby=lobby, state=2)
    message = {}
    if results.count() > 0:
        if action == 0:
            results[0].state = 0
            results[0].save()
            message["text"] = "Rejected invitation from %s for %s" % (results[0].issuer, lobby)
            return Success(message)
        else:
            if lobby.players.count() < lobby.max_players:
                if user not in lobby.players.all():
                    assoc = PlayersLobby(lobby=lobby, player=user)
                    assoc.save()
                    results[0].state = 1
                    results[0].save()
                    message["text"] = "Accepted invitation from %s for %s" % (results[0].issuer, lobby)
                    return Success(message)
                else:
                    message["text"] = "You are already in the lobby %s" % lobby
                    return Failure(message)
            else:
                message["text"] = "Lobby %s is already full" % lobby
                return Failure(message)
    else:
        message["text"] = "This invitation does not exist anymore"
        return Failure(message)