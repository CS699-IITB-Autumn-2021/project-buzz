document.addEventListener('DOMContentLoaded', () =>{
    var socket = io();

    // rendering messages in the message display area
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_time_stamp = document.createElement('span');
        const br = document.createElement('br');
        span_username.innerHTML = data.username;
        span_time_stamp.innerHTML = data.time_stamp;
        p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time_stamp.outerHTML;
        document.querySelector('#messages-display-area').append(p);
    })

    // sending message to the server on button click
    document.querySelector('#send-message-button').onclick = () => {
        socket.send({'msg': document.querySelector('#user-text').value, 'username': username});

        //clear the input
        document.querySelector('#user-text').value = '';
    }
})