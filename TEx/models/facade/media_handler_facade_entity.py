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

    def is_image(self) -> bool:
        """Return if Downloaded Image are an Image."""
        return self.content_type in ['image/gif', 'image/jpeg', 'image/png', 'image/webp', 'application/gif']

    def is_video(self) -> bool:
        """Return if Downloaded Image are a Video."""
        return self.content_type in ['application/ogg', 'video/mp4', 'video/quicktime', 'video/webm']

    def allow_search_in_text_file(self) -> bool:
        """Return if Allow to Find in the Text File."""
        return self.content_type in [
            'application/atom+xml',
            'application/bittorrent',
            'application/csv',
            'application/html',
            'application/json',
            'application/ld+json',
            'text/csv',
            'text/html',
            'text/plain',
            'text/xml',
        ]
