from fastapi import APIRouter, Depends, HTTPException
from ..schemas.user import UserCreate
from ..security.database import SessionLocal,get_db
from ..models import User
from ..security import auth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/user",tags=['user'])

@router.post("/login")
def user_login(user:UserCreate,db= Depends(get_db)):
    result = db.query(User).filter(User.username==user.username).first()
    if not result :
        raise HTTPException(status_code=404,detail="user not found.")
    if not auth.verify_password(user.password,result.password):
        raise HTTPException(status_code=404,detail="Invalid Credentials")
    if not result.is_active == True :
        raise HTTPException(status_code=404,detail="user is inactive")
    ## For JWT TOKEN
    access_token = auth.create_access_token({'sub':result.username})
    return {"Message":"Login Successfull","token":access_token , "token_type":"bearer"}

@router.get("/get")
def get_user(db = Depends(get_db)):
    users = db.query(User).all()
    return {"Message":"User Fetched Successfully","Data":users}

@router.get("/get/{id}")
def get_user(id:int ,db = Depends(get_db)):
    users = db.query(User).filter(User.id==id).first()
    if not users:
        raise HTTPException(status_code=404,detail="user not found.")
    return {"Message":"User Fetched Successfully","Data":users}

@router.post("/add")
def add_user(user:UserCreate,db = Depends(get_db)):
    # new_user = User(**user.model_dump())
    new_user = User(username=user.username,password=auth.hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/update")
def update_user(user:UserCreate,id:int,db= Depends(get_db)):
    users = db.query(User).filter(User.id==id).first()
    if not users:
        raise HTTPException(status_code=404,detail="user not found.")
    for key, value in user.model_dump().items():
        setattr(users, key , value)
    db.commit()
    db.refresh(users)
    return {"Message":"User Updated Successfully","Data":users}

@router.delete("/delete")
def delete_user(id:int,db= Depends(get_db)):
    users = db.query(User).filter(User.id==id).first()
    if not users:
        raise HTTPException(status_code=404,detail="user not found.")
    db.delete(users)
    db.commit()
    return {"Message":"User Deleted Successfully","Data":users}


@router.post("/token")
def get_token(form_data:OAuth2PasswordRequestForm = Depends(),db = Depends(get_db)):
    result = db.query(User).filter(User.username==form_data.username).first()
    if not result :
        raise HTTPException(status_code=404,detail="user not found.")
    if not auth.verify_password(form_data.password,result.password):
        raise HTTPException(status_code=404,detail="Invalid Credentials")
    if not result.is_active == True :
        raise HTTPException(status_code=404,detail="user is inactive")
    ## For JWT TOKEN
    access_token = auth.create_access_token({'sub':result.username})
    return {"access_token":access_token , "token_type":"bearer"}




