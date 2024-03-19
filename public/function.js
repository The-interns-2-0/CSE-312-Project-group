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

