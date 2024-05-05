from pydantic import BaseModel, EmailStr


class Playlist(BaseModel):
    keyword: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "keyword": "Korean Soft Indie"
                }
            ]
        }
    }


class ArtistList(BaseModel):
    names: list[str]


class User(BaseModel):
    email: EmailStr
    password: str
    name: str


class Content(BaseModel):
    genre: str
    mood: str
    color: str
    characteristics: list[str]
    artists: list[dict]
    tracks: list[dict]
    playlist: dict


class DiagnosisOut(BaseModel):
    content: Content
