const token = document.cookie.split("; ").find((row) => row.startsWith("token="))?.split("=")[1];
console.log((token));

const body = document.getElementById("main");
body.style.display = "none";


async function ServerResponse()
{
    try{
        const response = await fetch(`http://192.168.1.109:8000/verify/token/${token}`);
        const responseData = await response.json();

        if(responseData.detail == "Verified Token")
        {
            body.style.display = "block";
            let form = document.getElementById("join-form");

            form.addEventListener("submit", (e) => {
                e.preventDefault();
            
                let inviteCode = e.target.invite_link.value;
                window.location = `peerToPeer.html?room=${inviteCode}`;
            });
            
            const logout = document.getElementById("logout");
            console.log(logout);
            logout.addEventListener("click", (e) => {
                e.preventDefault();
                if (confirm("Logout!!! Are you sure?") == true)
                {
                    window.location.href = "signin.html";
                } 
            })
        }
        else
        {
            alert("Please Log In To Your Account.");
            window.location.reload();
            window.location.href = "signIn.html";
        }
    }
    catch(err)
    {
        alert("Server Is Currently Unavailabe");
        console.log(err);
    }
}

ServerResponse();