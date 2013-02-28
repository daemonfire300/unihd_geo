# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/member/login/')
def index(request):
    userprofile = request.user.userprofile
    print userprofile.friends.all()
    return render(request, 'member/index.html', {"profile": userprofile})