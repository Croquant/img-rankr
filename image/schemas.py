from datetime import datetime

from ninja import Field, Schema


class ImageSchema(Schema):
    file_url: str
    file_hash: str
    created_at: datetime
    modified_at: datetime
    score: float = Field(None, alias="elo.score")


class AddImageInputSchema(Schema):
    file_url: str


class AddImageResponseSchema(Schema):
    created: bool
    image: ImageSchema


class AddImageErrorSchema(Schema):
    created: bool
    error_message: str
