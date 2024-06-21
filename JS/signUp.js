
// For Navbar
let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('open')
};
// For Navbar





//test code
    const first_nameBox = document.getElementById('firstName');
    const last_nameBox = document.getElementById('lastName');
    const emailBox = document.getElementById('email');
    const occupationBox = document.getElementById('occupation');
    const passwordBox = document.getElementById("password");
    const confirmPasswordBox = document.getElementById("confirm-password");
    const otpBox = document.getElementById("otp");
    let signUpBox = document.getElementById("signUp");
    let verifyBox = document.getElementById("verifyOTP");

    otpBox.style.display = "none";
    verifyBox.style.display = "none";
//


const form = document.getElementById("user_form");

form.addEventListener("submit", async (e) =>{
    
    e.preventDefault();
    console.log("1 is clicked");
    
    const email = emailBox.value;
    const password = passwordBox.value;
    const confirmPassword = confirmPasswordBox.value;

    if(password != confirmPassword)
    {
        return alert("Password Do Not Match");
    }

    else
    {
        try
        {
            URL = `http://127.0.0.1:8000/checkemail/${email}`;
            let response = await fetch(URL);
            if (response.ok)
            {
                console.log("Ok");
            } 
            else 
            {
                console.log("not Ok");
            }
            const responseData = await response.json();


            if(responseData.detail == "Used")
            {
                return alert("You Have Already Created An Account With This Email")
            }

            else
            {

                try
                {
                    URL = `http://127.0.0.1:8000/otp/send/${email}`;
                    let response = await fetch(URL);
                    if (response.ok)
                    {
                        console.log("Ok");
                    } 
                    else 
                    {
                        console.log("not Ok");
                    }
                    const responseData = await response.json();

                    if(responseData.detail != "Limit Exceed")
                    {
                        // beforing sending the otp making all input box not editable
                        first_nameBox.readOnly = true
                        last_nameBox.readOnly = true
                        emailBox.readOnly = true
                        occupationBox.readOnly = true
                        passwordBox.readOnly = true
                        confirmPasswordBox.readOnly = true

                        // buttonBox.innerHTML = "Verify Your Email";


                        // Display the OTP Input Box
                        otpBox.style.display = "block";
                        otpBox.required = true;
                        signUpBox.style.display = "none";
                        verifyBox.style.display = "block";

                        alert("We Sent An OTP Your Email/nPlease Verify Your Email");
                        

                    }
                    else
                    {
                        alert("Limit Exceed, You Have Tried Too Many Time\nPlease Try Again Tomorrow");
                    }

                }
                catch(err)
                {
                    console.log("From OTP Block", err);
                }
                        
                
                
            }
        }
        catch(err)
        {
            alert("Server Is Currently Unavailabe");
            console.log(err);
        }
        // checking if the email is already registered
    }

})


verifyBox.addEventListener("click", async (e) =>{
    const first_name = first_nameBox.value;
    const last_name = last_nameBox.value;
    const email = emailBox.value;
    const occupation = occupationBox.value;
    const password = passwordBox.value;
    const otp = otpBox.value;

    // Verifing the OTP user provived
    const otpVerifyResponse = await fetch(`http://127.0.0.1:8000/otp/verify/${email}/${otp}`);
    const otpVerifyResponseData = await otpVerifyResponse.json();

    if(otpVerifyResponseData.detail == "Verified")
    {
        // Deleting the otp record for this email
        await fetch(`http://127.0.0.1:8000/otp/delete${email}`, {method: "DELETE"});
        
        const data = {
            first_name,
            last_name,
            email,
            occupation,
            password,
        };
        // console.log(JSON.stringify(data));
        const response = await fetch("http://127.0.0.1:8000/registration/", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
    
        if (response.ok) {
            console.log("Ok");
        } else {
            console.log("not Ok");
        }
    
        const responseData = response.json();
        console.log('API response:', responseData); // Handle successful response
    
        alert("Account Created Successfully");
        window.location.reload();
        window.location.href = "signIn.html";
    }
    else
    {
        alert("WRONG OTP, Check Your Email");
    }

                            // const data = {
                            //     first_name,
                            //     last_name,
                            //     email,
                            //     occupation,
                            // };
                            // // console.log(JSON.stringify(data));
                            // const response = await fetch("http://127.0.0.1:8000/registration/", {
                            //     method: 'POST',
                            //     headers: { 'Content-Type': 'application/json' },
                            //     body: JSON.stringify(data),
                            // });

                            // if (response.ok) {
                            //     console.log("Ok");
                            // } else {
                            //     console.log("not Ok");
                            // }

                            // const responseData = response.json();
                            // console.log('API response:', responseData); // Handle successful response

                            // alert("Account Created Successfully");
                            // // window.location.href = "signIn.html";

});