from fastapi import FastAPI,status,Body, HTTPException, Request, Form
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory = "templates")

message_db = []


class Message(BaseModel):
    id:int
    text:str




@app.post("/", status_code=status.HTTP_201_CREATED)
def create_message(request: Request, message: str = Form()) -> HTMLResponse:
    if len(message_db) == 0:
        max_id_message = 0
    else:
        max_id_message = max([i.dict()['id'] for i in message_db]) + 1
    message_db.append(Message(id=max_id_message, text=message))
    return templates.TemplateResponse("message.html", {"request": request, "messages": message_db})

@app.get("/")
async def get_all_messages(request:Request) -> HTMLResponse:
    return templates.TemplateResponse("message.html", {"request": request, "messages": message_db})

@app.get(path="/message/{message_id}")
async def get_message(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("message.html", {"request": request, "messages": message_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.put("/message/{message_id}")
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = message_db[message_id]
        edit_message.text = message
        return f"Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail = "Message not found")


@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    try:
        message_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/")
async def kill_message_all() -> str:
    return f"All messages deleted!"
