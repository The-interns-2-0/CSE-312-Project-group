const messages = document.getElementById("chat-messages");
function addchat() {
    const chat = document.getElementById("chatbox").value;
    const data = { chat: chat };
    
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
    
    ;
}
function sendmsg() {
    messages.innerHTML = "";
    fetch('/addchat')
    .then(response => response.json())
    .then(json => {
        // console.log(json);
        json.forEach(user_message => {
            // console.log(user_message);
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