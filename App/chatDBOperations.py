from bson import ObjectId
from App import chatDB

chat_rooms_collection = chatDB.get_collection("chat_rooms")
room_member_collection = chatDB.get_collection("room_member")
messages_collection = chatDB.get_collection("messages")


def saveRoom(room_name, createdBy, room_member2):
    room_id = chat_rooms_collection.insert_one({'room-name': room_name}).inserted_id
    add_room_member(room_id, room_name, createdBy)
    add_room_member(room_id, room_name, room_member2)
    return room_id


def add_room_member(room_id, room_name, member_to_add):
    room_member_collection.insert_one({'_id': {'room_id': ObjectId(room_id), 'username': member_to_add}, 'room_name': room_name})
    pass


def get_rooms_for_user(username):
    return list(room_member_collection.find({'_id.username': username}))


def is_room_member(room_id, username):
    return room_member_collection.count_documents({'_id': {'room_id': ObjectId(room_id), 'username': username}})
    pass


def save_message(room_id, data):
    messages_collection.insert_one({'room_id': room_id, 'data': data})
    pass


def get_room_by_roomname(room_name):
    return list(chat_rooms_collection.find({'room-name': room_name}))


def get_messages(room_id):
    return list(messages_collection.find({'room_id': room_id}))