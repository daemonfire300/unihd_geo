from django_socketio import events
import datetime
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

@events.on_connect
def global_chat_connect_handler(request, socket, context):
    socket.send_and_broadcast({"message": "user connected", "display": True})

 
@events.on_message(channel="^global_chat")
def global_chat_handler(request, socket, context, message):
    if message["session_key"]:
        session = Session.objects.get(session_key=message['session_key'])
        uid = session.get_decoded().get('_auth_user_id')
        request.user = User.objects.get(pk=uid)
        print "%s connected a" % request.user
    else:
        socket.send_and_broadcast({"message": message["message"], "timestamp": datetime.datetime.today().ctime(), "username": "%s" % request.user, "display": True})
        print "%s wrote something" % request.user