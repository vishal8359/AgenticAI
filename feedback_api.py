from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
app = FastAPI(title="Restaurant Feedback API")

#Request model for feedback
class Feedback(BaseModel):
    name: str
    rating: int
    comments: str

# POST endpoint to submit feedback
@app.post("/feedback")
def submit_feedback(feedback:Feedback, response_class=PlainTextResponse):
    return{
        "message" : "Thank You",
        "your_feedback" : {
            "name": feedback.name,
            "rating": feedback.rating,
            "comments": feedback.comments
        }
    }