from flask_socketio import send, join_room, leave_room
from App import socketio
from time import localtime, strftime


# event buckets for chat application
@socketio.on('message')
def message(data):
    print("\n\n{}\n\n".format(data))
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%M%p', localtime())},
         room=data['room'])
    # emit('some-event', 'this is a custom event message')
    pass


@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data['room'] + " room"}, room=data['room'])
    pass


@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + " room"}, room=data['room'])
    pass