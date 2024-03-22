function send_reg() {
    const user = document.getElementById("reg_user").value;
    const pass = document.getElementById("reg_pass").value;
    const data = { user: user, pass: pass };
    
    fetch('/register', {
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


function login() {
    const user = document.getElementById("login_user").value;
    const pass = document.getElementById("login_passs").value;
    const data = { user: user, pass: pass };
    
    fetch('/register', {
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



function sendChat() {
    const chatTextBox = document.getElementById("chat-text-box");
    const message = chatTextBox.value;
    chatTextBox.value = "";
    console.log("llllll")

    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({'messageType': 'chatMessage', 'message': message}));
    } else {
        const data = { message: message };
        fetch('/chat-messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {

            return response.json();
        })
        .then(json => {
            console.log(json); 
        })
        .catch(error => {
            console.error('catch error', error);
        });
    }

    chatTextBox.focus();
}

