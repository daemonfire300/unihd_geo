# import the logging library
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from member.forms import UserCreateForm
from django.http import HttpResponseRedirect
from lobbys.models import Invitation
from member.models import UserProfile
from member.models import Friendship
from common.http.jsonresponse import Failure, Success

@login_required(login_url='/member/login/')
def index(request):
    user = request.user.userprofile
    lobby_invitations = Invitation.objects.filter(player=user, state=2)
    return render(request, 'member/index.html', {"profile": user, "invitations": lobby_invitations})

@login_required(login_url='/member/login/')
def accept_friendrequest(request, friend_id, action):
    user = request.user.userprofile
    message = {}
    try:
        friend = UserProfile.objects.get(pk=friend_id)
        if Friendship.objects.filter(own_profile=user, friend_profile=friend).count() > 0:
            message["text"] = "You already handled this request"
            return Failure(message)    
        else:
            with transaction.commit_on_success():
                assoc = Friendship(own_profile=user, friend_profile=friend, accepted=bool(action))
                reverse_assoc = Friendship.objects.filter(own_profile=friend, friend_profile=user)[0]
                reverse_assoc.accepted = bool(action)
                reverse_assoc.save()
                assoc.save()
                message["text"] = "Done"
                return Success(message)
    except ObjectDoesNotExist:
        message["text"] = "Request or user does not exist"
        return Failure(message)
    
@login_required(login_url='/member/login/')
def send_friendrequest(request, friend_id):
    user = request.user.userprofile
    message = {}
    try:
        friend = UserProfile.objects.get(pk=friend_id)
        if Friendship.objects.filter(own_profile=user, friend_profile=friend).count() > 0:
            message["text"] = "You already send this request"
            return Failure(message)    
        else:
            if Friendship.objects.filter(own_profile=friend, friend_profile=user).count() > 0:
                with transaction.commit_on_success():
                    assoc = Friendship(own_profile=user, friend_profile=friend, accepted=True)
                    reverse_assoc = Friendship.objects.filter(own_profile=friend, friend_profile=user)[0]
                    reverse_assoc.accepted = True
                    reverse_assoc.save()
                    assoc.save()
                    message["text"] = "Done"
                    return Success(message)
            else:
                assoc = Friendship(own_profile=user, friend_profile=friend)
                assoc.save()
                message["text"] = "Done"
                return Success(message)
    except ObjectDoesNotExist:
        message["text"] = "Request or user does not exist"
        return Failure(message)

def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print new_user
            return HttpResponseRedirect("/member/profile")
    else:
        form = UserCreateForm()
    return render(request, 'member/register.html', {'form': form})
        