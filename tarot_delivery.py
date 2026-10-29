"""Low-bandwidth Tarot delivery: reuse bot-specific Telegram file_ids.

No image bytes, URLs, HTTP fetches, external downloaders or database access.
Optional manifest is read at most once per process/path (max two paths).
Invalid assets are disabled after failed delivery until process restart.
"""
import os
from functools import lru_cache
from types import MappingProxyType

from tarot_media import load_media_registry, card_photo_file_id

@lru_cache(maxsize=2)
def cached_photo_registry(path: str):
    """Manifest is deployment configuration. Restart to replace it safely."""
    return MappingProxyType(load_media_registry(path))

def valid_file_id(value) -> bool:
    return (isinstance(value,str)
            and 4 <= len(value) <= 512
            and value == value.strip()
            and not any(c.isspace() or c in "/\\:" for c in value))

class TarotAssetPolicy:
    def __init__(self, max_rejections=80):
        if type(max_rejections) is not int or max_rejections<=0:
            raise ValueError("Positive asset rejection limit required")
        self.max_rejections=max_rejections
        self._bad_ids=set()

    def enabled(self):
        return os.environ.get("TAROT_MEDIA_MODE","telegram").strip().lower() != "text"

    def asset(self, file_id):
        """Return a reusable file_id or None, never a binary file or URL."""
        if not self.enabled() or not valid_file_id(file_id):
            return None
        return file_id if file_id not in self._bad_ids else None

    def photo(self,card,path):
        if not self.enabled() or not path:
            return None
        return self.asset(card_photo_file_id(card,cached_photo_registry(path)))

    def mark_failed(self,file_id):
        """Remember asset failures in bounded RAM; do not retry costly uploads."""
        if valid_file_id(file_id) and len(self._bad_ids)<self.max_rejections:
            self._bad_ids.add(file_id)
