from django_socketio import events
import datetime
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from common.http.jsonresponse import AuthFailure
from common.http.jsonresponse import AuthSucces


"""
	global_chat_connect_handler.

	simply is fired if a user connects to ANY channel i.e. the socket server in general.
	This method is only used to register new incoming connections.
	No authentication can or should be done in here.

"""
@events.on_connect
def global_chat_connect_handler(request, socket, context):
    socket.send_and_broadcast({"message": "user connected", "display": True})

"""
	global_auth_handler.

	handles websocket requests issued to the the "auth_channel",
	this should be used to authenticate users via websocket with the socket server.
	NOTICE: I did not test this against a live environment, this means, that I am not sure, if this
	handler will log you in on the socket server AND the webserver. --> this is to be tested

	The auth_handler should take two parameters "username" and "password", which will be used to
	authenticate the user with the internal django authentication management.
	On success the handler returns python dictionary (decoded into a JSON object by the socket) which
	should contain the current (logged in) users session_key which should be used for further communication with the server.

"""
@events.on_message(channel="^auth_channel")
def global_auth_handler(request, socket, context, message):
	if len(message["username"]) > 4 and len(message["password"]) > 4:
		user = authenticate(username=message["username"], password=message["password"])
		if user is not None:
			login(request, user)
			session_key = request.session.session_key
			response = AuthSuccess(session_key)
			socket.send(response.get_content(json_encoded=False))
		else:
			response = AuthFailure(message="User is not authenticated")
	        socket.send(response.get_content(json_encoded=False))
	        print "Auth Error: %s" % request.user	


"""
	global_chat_handler.

	fired everytime a user submits a message on the "global_chat" channel.
	This handler will check if a request is signed with a valid session_key,
	and validates the user object returned against the authentication backend.
	Only authenticated (logged in) users should be eligable to send messages through this handler.
	
"""
@events.on_message(channel="^global_chat")
def global_chat_handler(request, socket, context, message):
    if message["session_key"]:
        session = Session.objects.get(session_key=message['session_key'])
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        if user.is_authenticated:
        	request.user = user
        print "%s connected a" % request.user
    else:
    	response = AuthFailure(message="User is not authenticated")
        socket.send(response.get_content(json_encoded=False))
        print "Auth Error: %s" % request.user