from flask_socketio import send, join_room, leave_room, emit
from App import socketio
from time import localtime, strftime
from App.chatDBOperations import save_message, get_room_by_roomname, get_messages


@socketio.on('message')
def message(data):
    """
    This function is to handle message event on the server side, it sends a incoming message from a single client to all
    all the connected clients of the chat room. It also saves the message in persistent storage so that if any user, who
    is not online can view it later.

    Inputs:
        :data: Its a python dictionary consisting of message, room name to which this was sent and the user who sent it
        :type data: JSON (can be accessed in python using Dictionary syntax)

    Returns:
        ::JSON format data which is to be sent to all connected clients of the room.(appending the timestamp from server
        side)
    """
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


@socketio.on('join')
def join(data):
    """
    This function handles the join room functionality

    Inputs:
        :data: A json format data sent by client consisting of user-name and the room-name which the user wants to join
        :type data: JSON (can be accessed in python using Dictionary syntax)

    Returns:
        ::A join room announcement to all connected clients of the chat room specified. (Type JSON)
    """
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
    """
        This function handles the leave room functionality

        Inputs:
            :data: A json format data sent by client consisting of user-name and the room-name which the user wants to
            leave
            :type data: JSON (can be accessed in python using Dictionary syntax)

        Returns:
            ::A leave room announcement to all connected clients of the chat room specified. (Type JSON)
        """
    if data['room']:
        leave_room(data['room'])

        # leave room announcement
        send({'msg': data['username'] + " has left the " + data['room']}, room=data['room'])
    pass