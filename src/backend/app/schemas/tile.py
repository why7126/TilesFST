from pydantic import BaseModel, Field

class TileImage(BaseModel):
    object_key: str
    url: str
    is_main: bool = False

class TileListItem(BaseModel):
    id: int
    name: str
    model: str
    category: str | None = None
    main_image_url: str | None = None

class TileDetail(BaseModel):
    id: int
    name: str
    model: str
    category: str | None = None
    color: str | None = None
    size: str | None = None
    description: str | None = None
    images: list[TileImage] = Field(default_factory=list)

class TileCreate(BaseModel):
    name: str
    model: str
    category: str | None = None
    color: str | None = None
    size: str | None = None
    description: str | None = None
