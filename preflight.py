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
        # Profile storage may be deliberately disabled, but variables must be paired.
        path=env.get("PROFILE_DB_PATH","").strip()
        key=env.get("PROFILE_ENCRYPTION_KEY","").strip()
        add("profile_config_paired",bool(path)==bool(key),
            "Set both PROFILE_DB_PATH and PROFILE_ENCRYPTION_KEY, or neither")
        if path and key:
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
        # Western natal is an opt-in, unpublished development preview.
        # Its JPL kernel is mandatory only if the operator enables the feature.
        kernel=env.get("JPL_EPHEMERIS_PATH","").strip()
        if env.get("ENABLE_WESTERN_NATAL","").strip()=="1":
            add("jpl_kernel_present",bool(kernel and Path(kernel).is_file()),
                "Existing local JPL BSP file required when Western natal is enabled")
            if kernel and Path(kernel).is_file():
                add("jpl_kernel_extension",Path(kernel).suffix.lower()==".bsp",
                    "Configured JPL ephemeris path should be a .bsp file")
        elif kernel:
            add("jpl_kernel_optional_path",Path(kernel).is_file(),
                "Configured optional JPL path must exist if provided")
        # Animation IDs are optional: bot.py implements a text-only fallback.
        # Recording them as warnings avoids blocking a valid text-only bot.
        for var in ("TAROT_REVEAL_FILE_ID","TAROT_SHUFFLE_FILE_ID"):
            if not env.get(var,"").strip():
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
