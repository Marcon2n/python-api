from typing import List
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: str = None
    username: str
    password: str

class RegisterResponse(BaseModel):
    message: str
    list: List[User]

userList: List[User] = []

@app.post('/register', response_model=RegisterResponse)
def register(user: User):
    if any(existing_user.username == user.username for existing_user in userList):
        raise HTTPException(status_code=400, detail="User đã tồn tại")
    
    new_user = User(
        id=str(uuid.uuid4()),
        username=user.username,
        password=user.password
    )
    userList.append(new_user)

    return {
        "message": "Tạo mới thành công",
        "list": userList
    }

@app.post('/login')
def login(user: User):
    for existing_user in userList:
        if existing_user.username == user.username:
            if existing_user.password == user.password:
                return {"message": "Login thành công"}
            else:
                raise HTTPException(status_code=400, detail="Mật khẩu không đúng")

    raise HTTPException(status_code=400, detail="Tài khoản không tồn tại")

@app.get('/users', response_model=List[User])
def get_all_users():
    return userList
