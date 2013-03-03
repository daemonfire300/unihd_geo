# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from member.forms import UserCreateForm
from django.http import HttpResponseRedirect
from lobbys.models import Invitation

@login_required(login_url='/member/login/')
def index(request):
    user = request.user.userprofile
    lobby_invitations = Invitation.objects.filter(player=user, state=2)
    return render(request, 'member/index.html', {"profile": user, "invitations": lobby_invitations})

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
        