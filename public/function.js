const messages = document.getElementById("chat-messages");
const ws=true;
// var socket = io.connect('wss://' + window.location.host + '/websocket');
const socket = io();
// var room_name = socket.request.headers.referer;
socket.on('connect', function() {
    console.log('Connected!');
})

socket.on('response', function(user_message) {
    console.log(user_message);
    messages.innerHTML += `<span><b><img src="${user_message.profile_pic}" height="20px" width="20px">${user_message.username}</b>: ${user_message.message}</span><br>`;
    messages.innerHTML +=`<button onclick='thumbs_up(\"` + user_message._id + `\")'>👍</button>:${user_message.thumbsup}`;
    messages.innerHTML +=`<button onclick='thumbs_down(\"` + user_message._id + `\")'>👎</button>:${user_message.thumbsdown}<br>`;
    messages.scrollIntoView(false);
    const chatMessages = document.getElementById("chatbox");
    chatMessages.value = "";
});
socket.on('lead', function(top) {
    fir=document.getElementById("1");
    sec=document.getElementById("2");
    thi=document.getElementById("3");
    fir.innerHTML = top[1]  ? top[1] : "None";
    sec.innerHTML = top[2]  ? top[2] : "None";
    thi.innerHTML = top[3]  ? top[3] : "None";

});

function addchat() {
    const chat = document.getElementById("chatbox").value;
    const data = { chat: chat };
    if (ws){
        socket.emit('message', data);
    }
    else{
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
};
}

function sendmsg() {
    messages.innerHTML = "";
    fetch('/addchat')
    .then(response => response.json())
    .then(json => {
        json.forEach(user_message => {
            messages.innerHTML += `<span><b><img src="${user_message.profile_pic}" height="20px" width="20px">${user_message.username}</b>: ${user_message.message}</span><br>`;
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