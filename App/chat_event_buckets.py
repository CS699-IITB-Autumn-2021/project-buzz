from flask_socketio import send, join_room, leave_room, emit
from App import socketio
from time import localtime, strftime
from App.chatDBOperations import save_message, get_room_by_roomname, get_messages


# event buckets for chat application
@socketio.on('message')
def message(data):
    list_of_rooms = get_room_by_roomname(data['room'])
    data['time_stamp'] = strftime('%b-%d %I:%M%p', localtime())
    save_message(list_of_rooms[0]['_id'], data)
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': data['time_stamp']},
         room=data['room'])
    pass


@socketio.on('join')
def join(data):
    join_room(data['room'])
    list_of_room = get_room_by_roomname(data['room'])
    room_id = list_of_room[0]['_id']
    list_of_messages = get_messages(room_id)
    if list_of_messages:
        for item in list_of_messages:
            emit('load-previous-messages', item['data'])
    send({'msg': data['username'] + " has joined the " + data['room']}, room=data['room'])
    pass


@socketio.on('leave')
def leave(data):
    if data['room']:
        leave_room(data['room'])
        send({'msg': data['username'] + " has left the " + data['room']}, room=data['room'])
    pass