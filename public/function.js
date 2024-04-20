const messages = document.getElementById("chat-messages");
const ws=true;
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    console.log('Connected!');
})
socket.on('response', function(user_message) {
    console.log(user_message);
    messages.innerHTML+=`<span><b>${user_message.username}</b>: ${user_message.message}</span><br>`;
    messages.innerHTML +=`<button onclick='thumbs_up(\"` + user_message._id + `\")'>👍</button>:${user_message.thumbsup}`;
    messages.innerHTML +=`<button onclick='thumbs_down(\"` + user_message._id + `\")'>👎</button>:${user_message.thumbsdown}<br>`;
    messages.scrollIntoView(false);
    const chatMessages = document.getElementById("chatbox");
    chatMessages.value = "";
});
function addchat() {
    const chat = document.getElementById("chatbox").value;
    const data = { chat: chat };
    if (ws){
        socket.emit('message', data);
    }else{
    fetch('/addchat', {
        method: 'POST',
        redirect: "follow",
        headers: {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin" : "*", 
            "Access-Control-Allow-Credentials" : true 
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data=>location.reload())
}
    
    ;
}
function sendmsg() {
    messages.innerHTML = "";
    // if (ws){
    //     var message = document.getElementById('message').value;
    //     socket.emit('message', message);

    // }else{
        
    fetch('/addchat')
    .then(response => response.json())
    .then(json => {
        // console.log(json);
        json.forEach(user_message => {
            messages.innerHTML+=`<span><b>${user_message.username}</b>: ${user_message.message}</span><br>`;
            messages.innerHTML +=`<button onclick='thumbs_up(\"` + user_message._id + `\")'>👍</button>:${user_message.thumbsup}`;
            messages.innerHTML +=`<button onclick='thumbs_down(\"` + user_message._id + `\")'>👎</button>:${user_message.thumbsdown}<br>`;
            messages.scrollIntoView(false);
            const chatMessages = document.getElementById("chatbox");
            chatMessages.innerHTML = "";
        });
    }
    )

}
function thumbs_up(id){
    const data = { id: id };
    fetch('/like', {
        method: 'POST',
        redirect: "follow",
        headers: {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin" : "*", 
            "Access-Control-Allow-Credentials" : true 
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data=>location.reload())
    
    ;
}

function thumbs_down(id){
    const data = { id: id };
    fetch('/dislike', {
        method: 'POST',
        redirect: "follow",
        headers: {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin" : "*", 
            "Access-Control-Allow-Credentials" : true 
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data=>location.reload())
    
    ;
}