// For Navbar
let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('open')
};
// For Navbar

const signInForm = document.getElementById("signInForm");

signInForm.addEventListener("submit", async (e) => {

    e.preventDefault()

    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    const data = {
        email,
        password
    }
    console.log(JSON.stringify(data));
    
    const response = await fetch("http://192.168.1.109:8000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data),
    });

    const responseData = await response.json()
    if (responseData.token_type == "bearer" && responseData.ac_type == "User")
    {
        const token = responseData.access_token;
        document.cookie = `token=${token}`;
        alert("Log In Successful.")
        window.location.reload();
        window.location.href = "lobby.html";
    }
    else if(responseData.token_type == "bearer" && responseData.ac_type == "Admin")
    {
        alert("Admin Log In Successful.")
    }
    else
    {
        alert("Invalid Username or Password.")
    }
});