from pydantic import BaseModel


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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "names": ["Zion.T", "10cm", "J_ust"]
                }
            ]
        }
    }
