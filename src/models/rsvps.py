

from datetime import datetime

from pydantic import BaseModel


class RSVPResponse(BaseModel):
    id: int
    event_id: int
    attendee_id: int
    created_at: datetime

class SingleRSVPResponse(BaseModel):
    rsvp: RSVPResponse