from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import random, smtplib, bcrypt
from email.message import EmailMessage


# For JWT TOKEN
from jose import jwt
from datetime import datetime, timedelta



# self module
import database, models, schemas, oauth2
from salt_date_time import get_date, get_time
from otp import get_otp, send_otp
# from hash import get_hash_password



app = FastAPI()
models.Base.metadata.create_all(bind = database.engine)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/registration/", tags=["Registration"], status_code = status.HTTP_201_CREATED)
def create_user(requested_user: schemas.UserBase, db: Session = Depends(get_db)):


    special_key = bcrypt.hashpw(requested_user.email.encode(), bcrypt.gensalt())
    salt = bcrypt.gensalt()

    new_user = models.User(first_name = requested_user.first_name, last_name = requested_user.last_name, email = requested_user.email, occupation = requested_user.occupation, special_key = special_key, salt = salt, ac_creation_date = get_date(), ac_creation_time = get_time())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    hashed_password = bcrypt.hashpw(requested_user.password.encode(), bcrypt.gensalt())
    hashed_special_key = bcrypt.hashpw(special_key, salt)

    
    

    new_user_password = models.Password(password = hashed_password, hashed_special_key = hashed_special_key)
    db.add(new_user_password)
    db.commit()
    db.refresh(new_user_password)

    return {"detail" : "User Created"}


@app.get("/checkemail/{email}", tags=["Registration"], status_code=status.HTTP_200_OK)
def is_created(email: str, db: Session = Depends(get_db)):
    result_set = db.query(models.User).filter(models.User.email == email).first()

    if result_set is None:
        return {"detail" : "NotUsed"}
    else:
        return {"detail" : "Used"}


@app.get("/otp/send/{email}", tags=["Registration"])
def send_otp(email: str, db: Session = Depends(get_db)):
    
    check_email = db.query(models.Otp).filter(models.Otp.email == email)
    genarated_otp = get_otp()
    

    if check_email.first() is None:
        counter = 1
        send_otp(genarated_otp, email)
        new_otp = models.Otp(otp = genarated_otp, email = email, counter = counter, used = 0)
        db.add(new_otp)
        db.commit()
        db.refresh(new_otp)
        return {"detail" : "OTP Sent Successfully"}

    elif check_email.first() is not None and check_email.first().counter < 5:
        
        check_email.update({models.Otp.counter : models.Otp.counter+1})
        db.commit()

        send_otp(check_email.first().otp, email)
        return {"detail" : "OTP Sent Successfully Again"}
    
    else:
        return {"detail" : "Limit Exceed"}



@app.get("/otp/verify/{email}/{otp}", tags=["Registration"])
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    result_set = db.query(models.Otp).filter(models.Otp.email == email).first()
    if result_set.otp == otp:
        return {"detail": "Verified"}
    else:
        return {"detail" : "Wrong"}


@app.delete("/otp/delete/{email}", tags=["Registration"], status_code=status.HTTP_204_NO_CONTENT)
def delete_otp(email: str, db: Session = Depends(get_db)):
    db.query(models.Otp).filter(models.Otp.email == email).delete()
    db.commit()
    return {"detail" : "Deleted"}







SECRET_KEY = "MY_Secret_Key_For_GolTable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



@app.post("/login", tags=["Authentication"], status_code=status.HTTP_200_OK)
def verify_user(requested_user: schemas.loginBase, db: Session = Depends(get_db)):

    check_user = db.query(models.User).filter(models.User.email == requested_user.email).first()
    if check_user is not None:
        
        password = requested_user.password
        salt = check_user.salt
        special_key = check_user.special_key
        hashed_special_key = bcrypt.hashpw(special_key.encode(), salt.encode())

        get_password = db.query(models.Password).filter(models.Password.hashed_special_key == hashed_special_key).first()
        if get_password is None:
            return {"detail" : "Server Error"}
        else:

            is_matched = bcrypt.checkpw(password.encode(), get_password.password.encode())
            is_admin = check_user.is_admin

            if is_matched and is_admin:
                # return {"detail" : "Authenticated"}
                access_token = create_access_token(data={"sub": check_user.email})
                return {"access_token" : access_token, "token_type" : "bearer", "ac_type" : "Admin"}
            elif is_matched:
                # return {"detail" : "Logged In"}
                access_token = create_access_token(data={"sub": check_user.email})
                return {"access_token" : access_token, "token_type" : "bearer", "ac_type" : "User"}
            else:
                return {"detail" : "Wrong Password"}
        

    else:
        return {"detail" : "Not Registered"}
    
@app.get("/alluser/", tags=["Admin"])
def get_all_user(db: Session = Depends(get_db)):
    result_set = db.query(models.User).all()
    return result_set

@app.get("/user/{email}", tags=["Admin"])
def get_user(email, db: Session = Depends(get_db)):
    result_set = db.query(models.User).filter(models.User.email == email).first()
    if result_set is not None:
        return result_set
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Such User")


@app.post("/admin", tags=["Admin"])
def create_admin(requested_admin: schemas.UserBase, db: Session = Depends(get_db)):

    special_key = bcrypt.hashpw(requested_admin.email.encode(), bcrypt.gensalt())
    salt = bcrypt.gensalt()
    new_admin = models.User(first_name = requested_admin.first_name, last_name = requested_admin.last_name, email = requested_admin.email, occupation = requested_admin.occupation, special_key = special_key, salt = salt, ac_creation_date = get_date(), ac_creation_time = get_time(), is_admin = True)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    hashed_password = get_hash_password(requested_admin.password)
    hashed_special_key = bcrypt.hashpw(special_key, salt)

    
    

    new_admin_password = models.Password(password = hashed_password, hashed_special_key = hashed_special_key)
    db.add(new_admin_password)
    db.commit()
    db.refresh(new_admin_password)

    return {"detail" : "Admin Created"}

@app.delete("/remove/user/{email}", tags=["Admin"])

def create_admin(email: str, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.email == email).delete()
    db.commit()

    return {"detail" : "Account Deleted"}


@app.get("/verify/token/{token}")
def verify_access_token(token, db: Session = Depends(get_db)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = decoded_token["sub"]
        check_email = db.query(models.User).filter(models.User.email == email).first()
        if check_email:
            return {"detail" : "Verified Token"}
        else:
            return {"detail" : "Invalid Token"}
    except:
        return {"detail" : "Invalid Token"}




def get_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0,9))
    return otp


def send_otp(otp, mail):
    from_mail = "supp0rt.goltable@gmail.com"
    password = "fjui klwg lpco tsat"
    to_mail = mail

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_mail, password)


    message = EmailMessage()
    message["Subject"] = "OTP Verification"
    message["From"] = from_mail
    message["To"] = to_mail
    message.set_content("Your OTP is: " + otp + "\nThank You From Team GolTable")

    server.send_message(message)
    return "Ok"


