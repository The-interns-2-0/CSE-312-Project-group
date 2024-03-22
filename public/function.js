function add() {
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