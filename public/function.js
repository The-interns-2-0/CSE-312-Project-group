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
    ;
}
function sendmsg() {
    console.log("send");
    messages.innerHTML = "";
    
    fetch('/addchat')
    .then(response => response.json())
    .then(json => {
        // console.log(json);
        json.forEach(user_message => {
            // console.log(user_message);
            messages.innerHTML+=`<span><b>${user_message.username}</b>: ${user_message.message}</span><br>`;
            messages.scrollIntoView(false);
        });
    }
    )
}