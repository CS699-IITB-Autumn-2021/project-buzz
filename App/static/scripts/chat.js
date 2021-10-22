document.addEventListener('DOMContentLoaded', () => {
    let msg = document.querySelector('#user-text')
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        if(event.keyCode === 13){
            document.querySelector('#send-message-button').click();
        }
    })
})