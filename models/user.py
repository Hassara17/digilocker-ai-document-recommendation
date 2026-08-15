from pydantic import BaseModel

class User(BaseModel):

    age: int

    occupation: str

    state: str

    vehicle_owner: bool

    taxpayer: bool

    student: bool

    existing_documents: list[str]