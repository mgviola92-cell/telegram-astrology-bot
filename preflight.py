"""Safe release preflight for the native Telegram astrology bot.

No Telegram network calls, no kernel auto-download, no secret values printed.
Exit 1 on any required failed check. Use --mode ci for source-level dependency
readiness and --mode deploy for actual runtime secrets, storage and JPL kernel.
"""
import argparse
import importlib
import os
import sqlite3
import sys
from pathlib import Path

DEPENDENCIES = {
    "aiogram": "Telegram native bot",
    "lunar_python": "Four Pillars / Da Yun",
    "skyfield": "Western geocentric positions",
    "cryptography": "Encrypted user birth profiles",
}

def inspect_environment(*, mode="ci", environ=None):
    if mode not in ("ci","deploy"):
        raise ValueError("mode must be ci or deploy")
    env=os.environ if environ is None else environ
    checks=[]
    def add(name,passed,detail):
        checks.append({"name":name,"passed":bool(passed),"detail":detail})
    add("python",sys.version_info[:2]>=(3,12),"Python 3.12 or newer required")
    for package,feature in DEPENDENCIES.items():
        try:
            imported=importlib.import_module(package)
            ok=True
        except (ImportError, OSError):
            ok=False
        add("dependency:"+package,ok,feature)
    add("sqlite",sqlite3.sqlite_version_info>=(3,24,0),"SQLite UPSERT support")
    if mode=="deploy":
        token=env.get("TELEGRAM_BOT_TOKEN","").strip()
        add("telegram_token",bool(token and ":" in token and not token.startswith(":")),
            "Telegram token must be present in secret environment; value never printed")
        # Render Web Services need an HTTPS webhook, not polling without PORT.
        # Render automatically supplies the public origin. Never log secrets.
        from render_webhook import webhook_configuration
        try:
            webhook_configuration(env)
            webhook_config_ok=True
        except (ValueError,TypeError):
            webhook_config_ok=False
        add("render_webhook_config",webhook_config_ok,
            "Render web services require an auto-supplied HTTPS origin, a 32+ character TELEGRAM_WEBHOOK_SECRET and a valid PORT")
        # Profile storage may be deliberately disabled, but variables must be paired.
        path=env.get("PROFILE_DB_PATH","").strip()
        key=env.get("PROFILE_ENCRYPTION_KEY","").strip()
        add("profile_config_paired",bool(path)==bool(key),
            "Set both PROFILE_DB_PATH and PROFILE_ENCRYPTION_KEY, or neither")
        if path and key:
            if env.get("RENDER"):
                add("render_profile_persistence_confirmed",
                    env.get("PROFILE_PERSISTENT_DISK_CONFIRMED")=="1",
                    "Render SQLite birth profiles require a verified paid persistent disk; free web service filesystem is ephemeral")
            try:
                from cryptography.fernet import Fernet
                Fernet(key.encode("ascii"))
                valid_key=True
            except (ValueError, TypeError, UnicodeError, ImportError):
                valid_key=False
            add("profile_key_format",valid_key,"Fernet encryption key format")
            parent=Path(path).expanduser().parent
            add("database_directory",parent.is_dir() and os.access(parent,os.W_OK),
                "Persistent SQLite destination parent must already exist and be writable")
        group_db=env.get("GROUP_SETTINGS_DB_PATH","").strip()
        if group_db and path:
            add("group_db_separate_from_birth_profiles",
                Path(group_db).expanduser().resolve()
                !=Path(path).expanduser().resolve(),
                "Group settings SQLite must not reuse the birth-profile database file")
        if group_db:
            if env.get("RENDER"):
                add("render_group_settings_disk_confirmed",
                    env.get("GROUP_SETTINGS_PERSISTENT_DISK_CONFIRMED")=="1",
                    "Render group settings require a verified paid persistent disk")
            add("group_settings_db_directory",
                Path(group_db).expanduser().parent.is_dir()
                and os.access(Path(group_db).expanduser().parent,os.W_OK),
                "Group settings SQLite directory must exist and be writable")
            add("group_settings_db_not_memory",group_db!=":memory:",
                "Group settings durable DB cannot be :memory:")
        # Independent review and explicit enablement are separate flags.
        natal_flag=env.get("ENABLE_WESTERN_NATAL","").strip()
        add("natal_flag_valid",natal_flag in ("","0","1"),
            "ENABLE_WESTERN_NATAL must be unset, 0 or 1")
        if natal_flag=="1":
            add("natal_release_review_approved",
                env.get("WESTERN_NATAL_REVIEW_APPROVED","").strip()=="1",
                "Independent benchmark review and owner authorization must precede Western natal activation")
        # A local JPL kernel alone is not an external benchmark.
        kernel=env.get("JPL_EPHEMERIS_PATH","").strip()
        if natal_flag=="1":
            add("jpl_kernel_present",bool(kernel and Path(kernel).is_file()),
                "Existing local JPL BSP file required when Western natal is enabled")
            if kernel and Path(kernel).is_file():
                add("jpl_kernel_extension",Path(kernel).suffix.lower()==".bsp",
                    "Configured JPL ephemeris path should be a .bsp file")
        elif kernel:
            add("jpl_kernel_optional_path",Path(kernel).is_file(),
                "Configured optional JPL path must exist if provided")
        media_mode=env.get("TAROT_MEDIA_MODE","telegram").strip().lower()
        add("tarot_media_mode",media_mode in ("telegram","text"),
            "TAROT_MEDIA_MODE must be telegram or text; configured Telegram file_ids are reusable, not uploaded")
        # Tarot photo manifest is a filesystem path to a small JSON mapping.
        # Never expose the path, keys or Telegram file_ids in diagnostics.
        manifest=env.get("TAROT_CARD_PHOTOS_JSON","").strip()
        if manifest:
            try:
                from tarot_media import load_media_registry, coverage
                mapped=coverage(load_media_registry(manifest))["mapped"]
                manifest_ok=True
            except (OSError,ValueError,TypeError,UnicodeError):
                mapped=0
                manifest_ok=False
            add("tarot_manifest_valid",manifest_ok,
                "Configured TAROT_CARD_PHOTOS_JSON must point to a valid small JSON file of Telegram file IDs")
            if manifest_ok:
                checks.append({"name":"optional:tarot_photo_coverage","passed":True,
                               "detail":f"Configured {mapped}/78 Tarot card IDs; unmapped cards have text/animation fallback"})
        from tarot_delivery import valid_file_id
        for var in ("TAROT_REVEAL_FILE_ID","TAROT_SHUFFLE_FILE_ID"):
            asset=env.get(var,"").strip()
            if asset:
                add("tarot_asset_valid:"+var,valid_file_id(asset),
                    "A configured asset must be a Telegram file_id, not a URL or filesystem path")
            else:
                checks.append({"name":"optional:"+var,"passed":True,
                               "detail":"Not configured; native text fallback remains available"})
    return {"mode":mode,"passed":all(x["passed"] for x in checks),
            "checks":checks}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("ci","deploy"),default="ci")
    args=p.parse_args(argv)
    result=inspect_environment(mode=args.mode)
    for item in result["checks"]:
        print(("[PASS] " if item["passed"] else "[FAIL] ")
              +item["name"]+": "+item["detail"])
    print("Preflight: "+("PASS" if result["passed"] else "FAIL"))
    return 0 if result["passed"] else 1

if __name__=="__main__":
    raise SystemExit(main())
