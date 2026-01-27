from fastapi import FastAPI, HTTPException
import uvicorn
from typing import List
from model import Event
from datetime import date

proj = FastAPI(title="AI Event Assistant")
events_db: List[Event] = [
    Event(
        id=1,
        title="AI Bootcamp",
        date="2025-10-24",
        organiser="Tech Club",
        city="Banglore",
        email="host@gmail.com"
    ),
    Event(
        id=2,
        title="AI Webinar 2025",
        date="2025-11-30",
        organiser="XYZ Tech",
        city="Chennai",
        email="support@gmail.com"
    )
]

@proj.get('/events')
def get_all_events():
    return events_db

@proj.get('/events/search')
def search_events(title: str, city: str="Delhi"):
    result = []
    for event in events_db:
        if event.title.lower().count(title.lower()) > 0 and event.city.lower() == city.lower():
            result.append(event)
    if len(result) > 0:
        return result
    return {"message" : "No events found with title containing" + title+" and city as "+ city}

@proj.get('/events/{event_id}')
def get_event(event_id: int):
    for event in events_db:
        if event.id == event_id:
            return {"Event details": event}
    return {"message":"Event with id "+ str(event_id) + " is not available."}

# create a new event
@proj.post("/events/add")
def create_event(event_id:int, title:str, date:date=date.today(), organiser: str=None, email:str=None, city: str='Mumbai'):
    for event in events_db:
        if event.id == event_id:
            raise HTTPException(status_code=404, detail="Event already exists")
        
    event = Event(event_id, title, date, organiser, city, email)
    events_db.append(event)
    return {"message" : "Event created successfully", "event":event}

# put method - used when we need to replace the existing source on the server with another source
@proj.put('/events/replace/{event_id}')
def update_event(event_id:int, title:str, date:date=date.today(), organiser: str=None, email:str=None, city:str="Noida"):
    for i, event in enumerate(events_db):
        if event.id == event_id:
            updated_event= Event(event_id, title, date, organiser, email, city)
            events_db[i] = updated_event
            return {"message" : "Event Updated", "event":updated_event}
    raise HTTPException(status_code=404, detail="Event not found for updation")

# patch method - used when we need to edit only a part of an existing resource on the server instead of replacing entire resource

@proj.patch('/events/edit/{event_id}')
def change_event(event_id: int, title: str=None, date:date=None, organiser:str=None, city:str=None, email:str=None):
    for i, event in enumerate(events_db):
        if event.id == event_id:
            if title != None:
                event.title = title
            if date != None:
                event.date = date
            if organiser != None:
                event.organiser = organiser
            if city != None:
                event.city = city
            if email != None:
                event.email = email
            return {"message":"Event updated", "event":event}
    return {"error" : "Event not found"}

# delete method - used when we want to remove an existing resource from the server.
@proj.delete('/events/cancel/{event_id}')
def delete_event(event_id:int):
    for event in events_db:
        if event.id == event_id:
            events_db.remove(event)
            return {"message":f"Event with id {event_id} is deleted"}
    return {"error":"Event not found"}