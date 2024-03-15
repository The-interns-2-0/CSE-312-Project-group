function send_reg() {
    const user = document.getElementById("reg_user").value;
    const pass = document.getElementById("reg_pass").value;
    const data = { user: user, pass: pass };
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {response.json();})
}