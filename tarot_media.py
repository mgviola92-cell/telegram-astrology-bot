"""Optional Tarot art registry. Store Telegram file IDs, never media binaries.

Registry is a UTF-8 JSON object mapping an exact standard tarot card name
to one opaque Telegram photo file_id. Missing mappings deliberately fall back
to existing common animation/text in the bot. No image paths, URLs or network.
"""
import json
from pathlib import Path
from tarot_core import DECK

VALID_CARDS=frozenset(DECK)

def parse_media_registry(raw: str) -> dict[str,str]:
    try:
        obj=json.loads(raw)
    except (TypeError,ValueError) as exc:
        raise ValueError("Tarot media registry must be valid JSON") from exc
    if not isinstance(obj,dict):
        raise ValueError("Tarot media registry must be a JSON object")
    if not set(obj).issubset(VALID_CARDS):
        raise ValueError("Tarot media registry contains unknown card names")
    for card,file_id in obj.items():
        if (not isinstance(file_id,str) or not 4<=len(file_id)<=512
                or file_id!=file_id.strip() or any(ch.isspace() for ch in file_id)):
            raise ValueError("Every Tarot photo entry requires an opaque Telegram file_id")
        if "/" in file_id or "\\" in file_id or ":" in file_id:
            raise ValueError("Image paths and web URLs are forbidden; use Telegram photo file_id")
    return obj

def load_media_registry(path: str | None) -> dict[str,str]:
    if not path:
        return {}
    p=Path(path)
    if not p.is_file():
        raise ValueError("Configured Tarot media registry file does not exist")
    if p.stat().st_size>64_000:
        raise ValueError("Tarot media registry exceeds size limit")
    return parse_media_registry(p.read_text(encoding="utf-8"))

def card_photo_file_id(card: str, registry: dict[str,str]) -> str | None:
    if card not in VALID_CARDS:
        raise ValueError("Unknown Tarot card")
    return registry.get(card)

def coverage(registry: dict[str,str]) -> dict:
    missing=[card for card in DECK if card not in registry]
    return {"mapped":len(DECK)-len(missing),"total":len(DECK),
            "complete":not missing,"missing":missing}
