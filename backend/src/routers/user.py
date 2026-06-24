from fastapi import APIRouter, Depends, HTTPException
from ..schemas.user import UserCreate
from ..security.database import SessionLocal,get_db
from ..models import User


router = APIRouter(prefix="/user",tags=['user'])

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

@router.post("add")
def add_user(user:UserCreate,db = Depends(get_db)):
    new_user = User(**user.model_dump())
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




