from datetime import date

class Event:
    id: int
    title: str
    date: date
    organiser: str
    city: str
    email: str
    def __init__(self, id, title, date, organiser, city, email):
        self.id = id
        self.title = title
        self.date = date
        self.organiser = organiser
        self.city = city
        self.email = email
        