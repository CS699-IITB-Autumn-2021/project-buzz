// functions for toggling the side nav bar
function openNav() {
    document.getElementById("sidebar").style.width = "250px";
}

function closeNav() {
    document.getElementById("sidebar").style.width = "0";
}


// adding "press-enter" listener to "send" button in chat for better UX
document.addEventListener('DOMContentLoaded', () => {
    let msg = document.querySelector('#user-text')
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        if(event.keyCode === 13){
            document.querySelector('#send-message-button').click();
        }
    })
})