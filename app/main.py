
from fastapi import FastAPI, Depends, Query, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from . import models, database, schemas, crud
from sqlalchemy.orm import Session

from .database import get_db
from .user_loader import load_users

from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import math

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    db = database.SessionLocal()
    user_count = db.query(models.User).count()
    if user_count < 1000:
        await load_users(db, 1000 - user_count)
    db.close()

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    total = db.query(models.User).count()
    total_pages = math.ceil(total / limit)
    current_page = (skip // limit) + 1
    return templates.TemplateResponse("index.html", {
        "request": request,
        "users": users,
        "total": total,
        "page": current_page,
        "pages": total_pages,
        "limit": limit
    })

@app.get("/users", response_model=list[schemas.User])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_users(db, skip=skip, limit=limit)
@app.get("/random", response_class=HTMLResponse)
def show_random_user(request: Request, db: Session = Depends(get_db)):
    user = crud.get_random_user(db)
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return templates.TemplateResponse("random.html", {"request": request, "user": user})

@app.post("/load")
async def load_more_users(count: int = Form(...), db: Session = Depends(get_db)):
    await load_users(db, count)
    return RedirectResponse("/", status_code=303)

@app.get("/user/{user_id}", response_class=HTMLResponse)
def show_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user})
