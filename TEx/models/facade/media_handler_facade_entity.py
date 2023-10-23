"""Facade Entities for Media Handling."""

from pydantic import BaseModel


class MediaHandlingEntity(BaseModel):
    """Facade Entities for Media Handling."""

    media_id: int
    file_name: str
    content_type: str
    size_bytes: int
    disk_file_path: str
    is_ocr_supported: bool
