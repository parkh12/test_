from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Ticket
from pydantic import BaseModel

app = FastAPI()

class TicketCreate(BaseModel):
    age: int
    name: str
    price: int
    
@app.post("/tickets/")
def create_ticket(ticket:TicketCreate, db: Session=Depends(get_db)):
    new_ticket = Ticket(name=ticket.name, age=ticket.age, price=ticket.price)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@app.get("/tickets/")
def all_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all
    

@app.get("/tickets/{ticket_id}")
def search_ticket(ticket_id: int, db: Session=Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.get("tickets/age/")
def search_ticket_age(age:int, db:Session=Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.age == age).all()
    if not tickets:
        raise HTTPException(status_code=404, detail="not found")
    return tickets
    