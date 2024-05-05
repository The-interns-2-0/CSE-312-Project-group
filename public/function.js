const messages = document.getElementById("chat-messages");
const ws=true;
// var socket = io.connect('wss://' + window.location.host + '/websocket');
const socket = io();
// var room_name = socket.request.headers.referer;
socket.on('connect', function() {
    console.log('Connected!');
})

socket.on('response', function(user_message) {
    const id=document.getElementById(user_message._id)
    if (id){
        id.innerHTML=id.innerHTML.replace(id.innerHTML,user_message.message)
        return
    }

    messages.innerHTML += `<span><b><img src="${user_message.profile_pic}" height="20px" width="20px">${user_message.username}</b>:  <span id=${user_message._id}>${user_message.message}</span></span><br>`;
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
socket.on('error', function(top) {
    document.getElementById('content').innerHTML = 
    '<h1>Error 429 - Too Many Requests</h1>'
});
socket.on('start', function(data) {
    const left=data.left
    document.getElementById("left").innerHTML=left
    const right=data.right
    document.getElementById("right").innerHTML=right
    document.getElementById("gameinfo").innerHTML="You are in the game"
    const user_list=document.getElementById("user_list")
    console.log(data);
    data.users.forEach(
        user =>
        user_list.innerHTML+=user+"<br>"
    )
    document.getElementById("start-game-btn").innerHTML="Guess number"
    document.getElementById("start-game-btn").setAttribute("onclick", "guess()");
});
socket.on('continue', function(data) {
    const left=data.left
    document.getElementById("left").innerHTML=left
    const right=data.right
    document.getElementById("right").innerHTML=right
    console.log(data)
    console.log(data.number)
    document.getElementById("gameinfo").innerHTML="Player " + data.player + " tried " + data.number

});
socket.on('guesterror', function() {
    alert("no guess allow")
});
socket.on('join', function(data) {
    const user_list=document.getElementById("user_list")
    user_list.innerHTML+=data.user+"<br>"
});
socket.on('end', function(data) {
    const left="x"
    const right="x"
    document.getElementById("gameinfo").innerHTML="The game has ended"
    document.getElementById("winner-name").innerHTML=data.player
    document.getElementById("start-game-btn").innerHTML="Start Game"
    document.getElementById("start-game-btn").setAttribute("onclick", "startgame()");
    const user_list=document.getElementById("user_list")
    user_list.innerHTML=""
});


function startgame() {
    socket.emit('start');
}
function guess() {
    const chat = document.getElementById("guess-number").value;
    const data = { number: chat};
    socket.emit('guess', data);
}

function addchat() {
    const chat = document.getElementById("chatbox").value;
    var sec = document.getElementById("sec").value;
    if (!sec){
        sec=0;
    }
    const data = { chat: chat,sec: sec};
    console.log(sec);
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
            messages.innerHTML += `<span><b><img src="${user_message.profile_pic}" height="20px" width="20px">${user_message.username}</b>: <span id=${user_message._id}>${user_message.message}</span></span><br>`;
            messages.innerHTML +=`<button onclick='thumbs_up(\"` + user_message._id + `\")'>👍</button>:${user_message.thumbsup}`;
            messages.innerHTML +=`<button onclick='thumbs_down(\"` + user_message._id + `\")'>👎</button>:${user_message.thumbsdown}<br>`;
            messages.scrollIntoView(false);
            const chatMessages = document.getElementById("chatbox");
            chatMessages.innerHTML = "";
        });
    }
    )
    // fetch('/winner')
    // .then(response => response.json())
    // .then(player => {
    //     document.getElementById("winner").innerHTML=player
    // }
    // )

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
// document.addEventListener('DOMContentLoaded', function() {
//     function sendHeartbeat() {
//         socket.emit('loadmessage');
//     }

//     // Send heartbeat every second
//     setInterval(sendHeartbeat, 1000);
// });