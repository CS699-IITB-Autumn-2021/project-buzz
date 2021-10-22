from flask_socketio import send
from App import socketio
from time import localtime, strftime


# event buckets for chat application
@socketio.on('message')
def message(data):
    print("\n\n{}\n\n".format(data))
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%M%p', localtime())})
    # emit('some-event', 'this is a custom event message')