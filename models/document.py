from pydantic import BaseModel

class Document(BaseModel):
    document_name: str
    doctype: str
    issuer_id: str
    searchable: bool
    category: str