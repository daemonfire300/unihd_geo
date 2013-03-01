# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from lobbys.forms import LobbyCreationForm
from lobbys.models import Lobby

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
    return render(request, 'lobbys/show.html', {"lobby": lobby})
