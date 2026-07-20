import json
import pathlib
import datetime
import hashlib
import logging

USERS_FILE = pathlib.Path(__file__).parent.parent / "data" / "users.json"

def _load_users() -> dict:
    try:
        if USERS_FILE.exists():
            with open(USERS_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def _save_users(users: dict):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        logging.error("Failed to save users: " + str(e))

def _hash_email(email: str) -> str:
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()

def user_exists(email: str) -> bool:
    users = _load_users()
    return _hash_email(email) in users

def create_user(email: str, plan: str = "free") -> dict:
    users = _load_users()
    key = _hash_email(email)
    now = datetime.datetime.utcnow().isoformat()
    if key not in users:
        users[key] = {
            "email": email.lower().strip(),
            "plan": plan,
            "created": now,
            "last_login": now,
            "login_count": 1,
            "active": True,
        }
    else:
        users[key]["last_login"] = now
        users[key]["login_count"] = users[key].get("login_count", 0) + 1
    _save_users(users)
    return users[key]

def get_user(email: str) -> dict:
    users = _load_users()
    key = _hash_email(email)
    return users.get(key, {})

def get_trial_start(email: str, game_key: str):
    """Return persisted trial-start ISO timestamp for this email+game, or None."""
    user = get_user(email)
    if not user:
        return None
    return user.get("trials", {}).get(game_key)


def set_trial_start(email: str, game_key: str, iso_ts: str):
    """Persist a trial start against the user record. First write wins - never overwrites."""
    users = _load_users()
    key = _hash_email(email)
    if key in users:
        trials = users[key].setdefault("trials", {})
        if game_key not in trials:
            trials[game_key] = iso_ts
            _save_users(users)


def get_free_module(email: str):
    """Return the permanently chosen free module for this account, or None."""
    user = get_user(email)
    if not user:
        return None
    return user.get("free_module")


def set_free_module(email: str, module: str):
    """Persist the free module choice. First write wins - the choice is permanent."""
    users = _load_users()
    key = _hash_email(email)
    if key in users and not users[key].get("free_module"):
        users[key]["free_module"] = module
        _save_users(users)


def update_plan(email: str, plan: str):
    users = _load_users()
    key = _hash_email(email)
    if key in users:
        users[key]["plan"] = plan
        _save_users(users)

def deactivate_user(email: str):
    users = _load_users()
    key = _hash_email(email)
    if key in users:
        users[key]["active"] = False
        _save_users(users)

def get_all_users() -> list:
    users = _load_users()
    return list(users.values())

def get_user_count() -> dict:
    users = _load_users()
    total = len(users)
    paid = sum(1 for u in users.values() if u.get("plan") == "paid")
    free = total - paid
    active = sum(1 for u in users.values() if u.get("active", True))
    return {"total": total, "paid": paid, "free": free, "active": active}
