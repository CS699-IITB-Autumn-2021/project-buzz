from flask_socketio import send, join_room, leave_room, emit
from App import socketio
from time import localtime, strftime
from App.chatDBOperations import save_message, get_room_by_roomname, get_messages


# event buckets for chat application

# relaying message from a client to all other connected clients of the room
@socketio.on('message')
def message(data):
    if data['room'] is None:
        send({'msg': "Select a chat room to start chatting with a product owner"})
        send({'msg': "If you are not a part of any chat room till now: "})
        send({'msg': " -> To create a new room visit the \"details\" page of any product of your interest"})
        send({'msg': " -> Then click on \"chat with owner\" option"})
        return
    # fetching the room details of current_room
    list_of_rooms = get_room_by_roomname(data['room'])

    # adding timestamp for message from server side
    data['time_stamp'] = strftime('%b-%d %I:%M%p', localtime())

    # saving the message in persistent storage before displaying it to clients
    save_message(list_of_rooms[0]['_id'], data)

    # sending message to all connected clients of current room
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': data['time_stamp']},
         room=data['room'])
    pass


# handling join room functionality
@socketio.on('join')
def join(data):
    join_room(data['room'])

    # fetching room details using room name
    list_of_room = get_room_by_roomname(data['room'])
    room_id = list_of_room[0]['_id']

    # fetching previous messages of the new_room_to_join
    list_of_messages = get_messages(room_id)

    # sending all older messages of the room for display
    if list_of_messages:
        for item in list_of_messages:
            emit('load-previous-messages', item['data'])

    # sending announcement message/notification for the new joined user
    send({'msg': data['username'] + " has joined the " + data['room']}, room=data['room'])
    pass


@socketio.on('leave')
def leave(data):
    if data['room']:
        leave_room(data['room'])

        # leave room announcement
        send({'msg': data['username'] + " has left the " + data['room']}, room=data['room'])
    pass