# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from member.forms import UserCreateForm
from django.http import HttpResponseRedirect

@login_required(login_url='/member/login/')
def index(request):
    userprofile = request.user.userprofile
    return render(request, 'member/index.html', {"profile": userprofile})

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
        