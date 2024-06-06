from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()


# CORS 설정 추가
origins = ["http://127.0.0.1:5500", "http://18.210.66.19"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GuestbookEntry(BaseModel):
    id: int
    writer: str
    content: str
    timestamp: datetime

class GuestbookEntryCreate(BaseModel):
    writer: str
    content: str

guestbook_entries = []


@app.get("/")
async def welcome() -> dict:
    return {"msg" : "hello world"}

@app.get("/guestbook", response_model=List[GuestbookEntry])
async def read_guestbook():
    return guestbook_entries

@app.post("/guestbook", response_model=GuestbookEntry)
async def create_entry(entry: GuestbookEntryCreate):
    new_entry = GuestbookEntry(
        id=len(guestbook_entries) + 1,  
        writer=entry.writer,
        content=entry.content,
        timestamp=datetime.now()
    )
    guestbook_entries.append(new_entry)
    return new_entry

@app.delete("/guestbook/{entry_id}")
async def delete_entry(entry_id: int):
    for entry in guestbook_entries:
        if entry.id == entry_id:
            guestbook_entries.remove(entry)
            return {"message": "Entry deleted successfully"}
    return {"message": "Entry not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True) 
