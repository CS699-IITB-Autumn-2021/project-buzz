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
            // adding if block to add classes for styling messages of own-user and other-user messages for better UI/UX
            if(data.username == username){
                // adding class to own-user messages
                p.setAttribute("class", "own-message")

                // adding class for styling username
                span_username.setAttribute("class", "own-username")
                span_username.innerHTML = data.username;

                // adding claas to style the timestamp
                span_time_stamp.setAttribute("class", "timestamp")
                span_time_stamp.innerHTML = data.time_stamp;

                // appending message in message display area
                p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time_stamp.outerHTML;
                document.querySelector('#messages-display-area').append(p);
            } else {
                // adding class to other-user messages
                p.setAttribute("class", "other-message")

                // adding class for styling other's username
                span_username.setAttribute("class", "other-username")
                span_username.innerHTML = data.username;

                // adding claas to style the timestamp
                span_time_stamp.setAttribute("class", "timestamp")
                span_time_stamp.innerHTML = data.time_stamp;

                // appending message in message display area
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
        // changing appearance in side nav bar
        if(room){
            document.getElementById(room).style.backgroundColor = "";
            document.getElementById(room).style.color = "#F7F6F2";
        }

        // triggering leave event bucket on th server side
        socket.emit('leave', {'username': username, 'room': room});
   }

   // join room function
   function joinRoom(room){
        // changing appearance in side nav bar to display new joined room
        document.getElementById(room).style.backgroundColor = "#17a2b8";
        document.getElementById(room).style.color = "black";

        // triggering join event bucket on th server side
        socket.emit('join', {'username': username, 'room': room});

        // clearing the message area when user joins the room
        document.querySelector('#messages-display-area').innerHTML = ''
   }

   // Printing notifications to the room
   function PrintSystemNotification(msg){
        const p = document.createElement('p');
        // adding class to style system notifications
        p.setAttribute("class", "system-notification");
        p.innerHTML = msg;
        document.querySelector('#messages-display-area').append(p);
   }

   // loading previous messages when a user joins the room
   socket.on('load-previous-messages', data=>{
      if(data.msg){
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_time_stamp = document.createElement('span');
            const br = document.createElement('br');
             if (data.username){
                // adding if block to add classes for styling messages of own-user and other-user
                if(data.username == username){
                    // adding class to own-user messages
                    p.setAttribute("class", "own-message")

                    // adding class for styling username
                    span_username.setAttribute("class", "own-username")
                    span_username.innerHTML = data.username;

                    // adding claas to style the timestamp
                    span_time_stamp.setAttribute("class", "timestamp")
                    span_time_stamp.innerHTML = data.time_stamp;

                    // appending message in message display area
                    p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time_stamp.outerHTML;
                    document.querySelector('#messages-display-area').append(p);
                 } else {
                    // adding class to other-user messages
                    p.setAttribute("class", "other-message")

                    // adding class for styling other's username
                    span_username.setAttribute("class", "other-username")
                    span_username.innerHTML = data.username;


                    // adding claas to style the timestamp
                    span_time_stamp.setAttribute("class", "timestamp")
                    span_time_stamp.innerHTML = data.time_stamp;

                    // appending message in message display area
                    p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time_stamp.outerHTML;
                    document.querySelector('#messages-display-area').append(p);
                }
               }
            }
   })
})