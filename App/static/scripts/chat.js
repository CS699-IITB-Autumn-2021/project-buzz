function openNav() {
    document.getElementById("sidebar").style.width = "250px";
    // document.getElementById("chat-area").style.marginLeft = "150px";
}

function closeNav() {
    document.getElementById("sidebar").style.width = "0";
    // document.getElementById("chat-area").style.marginLeft = "0";
}

document.addEventListener('DOMContentLoaded', () => {
    let msg = document.querySelector('#user-text')
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        if(event.keyCode === 13){
            document.querySelector('#send-message-button').click();
        }
    })
})