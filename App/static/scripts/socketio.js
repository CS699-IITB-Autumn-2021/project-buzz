document.addEventListener('DOMContentLoaded', () =>{
    var socket = io();

    let current_room = null
    // rendering messages in the message display area
    socket.on('message', data => {
    if(data.msg){
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_time_stamp = document.createElement('span');
        const br = document.createElement('br');
        if (data.username){
            // adding if block to add classes for styling messages of own-user and other-user
            if(data.username == username){
                p.setAttribute("class", "own-message")

                span_username.setAttribute("class", "own-username")
                span_username.innerHTML = data.username;

                span_time_stamp.setAttribute("class", "timestamp")
                span_time_stamp.innerHTML = data.time_stamp;

                p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time_stamp.outerHTML;
                document.querySelector('#messages-display-area').append(p);
            } else {
                p.setAttribute("class", "other-message")

                span_username.setAttribute("class", "other-username")
                span_username.innerHTML = data.username;

                span_time_stamp.setAttribute("class", "timestamp")
                span_time_stamp.innerHTML = data.time_stamp;

                p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time_stamp.outerHTML;
                document.querySelector('#messages-display-area').append(p);
            }
        } else {
            PrintSystemNotification(data.msg);
        }
        }
    })

    // sending message to the server on button click
    document.querySelector('#send-message-button').onclick = () => {
        socket.send({'msg': document.querySelector('#user-text').value, 'username': username, 'room': current_room});

        //clear the input
        document.querySelector('#user-text').value = '';
    }

   // room selection
   document.querySelectorAll(".select-room").forEach(p => {
        p.onclick = () => {
            let new_room_to_join = p.innerHTML;
            if(new_room_to_join == current_room){
                msg = `You are already in ${current_room}`;
                PrintSystemNotification(msg);
            } else {
                leaveRoom(current_room);
                joinRoom(new_room_to_join);
                current_room = new_room_to_join;
            }
        }
   })

   // Leave room function
   function leaveRoom(room){
        if(room){
            document.getElementById(room).style.backgroundColor = "";
            document.getElementById(room).style.color = "#F7F6F2";
        }
        socket.emit('leave', {'username': username, 'room': room});
   }

   // join room function
   function joinRoom(room){
        document.getElementById(room).style.backgroundColor = "#17a2b8";
        document.getElementById(room).style.color = "black";
        socket.emit('join', {'username': username, 'room': room});
        // clearing the message area when user joins the room
        document.querySelector('#messages-display-area').innerHTML = ''
   }

   // Printing notifications to the room
   function PrintSystemNotification(msg){
        const p = document.createElement('p');
        p.setAttribute("class", "system-notification");
        p.innerHTML = msg;
        document.querySelector('#messages-display-area').append(p);
   }

   // loading previous messages
   socket.on('load-previous-messages', data=>{
      if(data.msg){
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_time_stamp = document.createElement('span');
            const br = document.createElement('br');
             if (data.username){
            // adding if block to add classes for styling messages of own-user and other-user
                if(data.username == username){
                    p.setAttribute("class", "own-message")

                    span_username.setAttribute("class", "own-username")
                    span_username.innerHTML = data.username;

                    span_time_stamp.setAttribute("class", "timestamp")
                    span_time_stamp.innerHTML = data.time_stamp;

                    p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time_stamp.outerHTML;
                    document.querySelector('#messages-display-area').append(p);
                 } else {
                    p.setAttribute("class", "other-message")

                    span_username.setAttribute("class", "other-username")
                    span_username.innerHTML = data.username;

                    span_time_stamp.setAttribute("class", "timestamp")
                    span_time_stamp.innerHTML = data.time_stamp;

                    p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time_stamp.outerHTML;
                    document.querySelector('#messages-display-area').append(p);
                }
               }
            }
   })
})