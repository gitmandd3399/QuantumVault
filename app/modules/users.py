import datetime
import hashlib
import logging
import json
import pathlib

_sb_client = None
_sb_tried = False

def _sb():
    global _sb_client, _sb_tried
    if _sb_tried:
        return _sb_client
    _sb_tried = True
    try:
        import streamlit as st
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
        if url and key:
            _sb_client = create_client(url, key)
    except Exception as e:
        logging.warning("Supabase unavailable, JSON fallback: " + str(e))
        _sb_client = None
    return _sb_client

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
    try:
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        logging.error("Failed to save users (JSON): " + str(e))

def _hash_email(email: str) -> str:
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()

def _row_to_user(row: dict) -> dict:
    if not row:
        return {}
    trials = row.get("trials") or {}
    if isinstance(trials, str):
        try:
            trials = json.loads(trials)
        except Exception:
            trials = {}
    return {
        "email": row.get("email", ""),
        "plan": row.get("plan", "free"),
        "free_module": row.get("free_module"),
        "trials": trials,
        "created": row.get("created"),
        "last_login": row.get("last_login"),
        "login_count": row.get("login_count", 1),
        "active": row.get("active", True),
    }

def user_exists(email: str) -> bool:
    sb = _sb()
    if sb:
        try:
            r = sb.table("users").select("email_hash").eq("email_hash", _hash_email(email)).execute()
            return bool(r.data)
        except Exception as e:
            logging.error("user_exists: " + str(e))
    return _hash_email(email) in _load_users()

def create_user(email: str, plan: str = "free") -> dict:
    sb = _sb()
    key = _hash_email(email)
    now = datetime.datetime.utcnow().isoformat()
    if sb:
        try:
            existing = sb.table("users").select("*").eq("email_hash", key).execute()
            if existing.data:
                row = existing.data[0]
                new_count = (row.get("login_count", 0) or 0) + 1
                sb.table("users").update({"last_login": now, "login_count": new_count}).eq("email_hash", key).execute()
                row["last_login"] = now
                row["login_count"] = new_count
                return _row_to_user(row)
            new_row = {"email_hash": key, "email": email.lower().strip(), "plan": plan,
                       "created": now, "last_login": now, "login_count": 1, "active": True, "trials": {}}
            sb.table("users").insert(new_row).execute()
            return _row_to_user(new_row)
        except Exception as e:
            logging.error("create_user: " + str(e))
    users = _load_users()
    if key not in users:
        users[key] = {"email": email.lower().strip(), "plan": plan, "created": now,
                      "last_login": now, "login_count": 1, "active": True}
    else:
        users[key]["last_login"] = now
        users[key]["login_count"] = users[key].get("login_count", 0) + 1
    _save_users(users)
    return users[key]

def get_user(email: str) -> dict:
    sb = _sb()
    if sb:
        try:
            r = sb.table("users").select("*").eq("email_hash", _hash_email(email)).execute()
            return _row_to_user(r.data[0]) if r.data else {}
        except Exception as e:
            logging.error("get_user: " + str(e))
    return _load_users().get(_hash_email(email), {})

def get_trial_start(email: str, game_key: str):
    user = get_user(email)
    if not user:
        return None
    return (user.get("trials") or {}).get(game_key)

def set_trial_start(email: str, game_key: str, iso_ts: str):
    sb = _sb()
    key = _hash_email(email)
    if sb:
        try:
            r = sb.table("users").select("trials").eq("email_hash", key).execute()
            if r.data:
                trials = r.data[0].get("trials") or {}
                if isinstance(trials, str):
                    trials = json.loads(trials)
                if game_key not in trials:
                    trials[game_key] = iso_ts
                    sb.table("users").update({"trials": trials}).eq("email_hash", key).execute()
            return
        except Exception as e:
            logging.error("set_trial_start: " + str(e))
    users = _load_users()
    if key in users:
        trials = users[key].setdefault("trials", {})
        if game_key not in trials:
            trials[game_key] = iso_ts
            _save_users(users)

def get_free_module(email: str):
    user = get_user(email)
    if not user:
        return None
    return user.get("free_module")

def set_free_module(email: str, module: str):
    sb = _sb()
    key = _hash_email(email)
    if sb:
        try:
            r = sb.table("users").select("free_module").eq("email_hash", key).execute()
            if r.data and not r.data[0].get("free_module"):
                sb.table("users").update({"free_module": module}).eq("email_hash", key).execute()
            return
        except Exception as e:
            logging.error("set_free_module: " + str(e))
    users = _load_users()
    if key in users and not users[key].get("free_module"):
        users[key]["free_module"] = module
        _save_users(users)

def update_plan(email: str, plan: str):
    sb = _sb()
    key = _hash_email(email)
    if sb:
        try:
            sb.table("users").update({"plan": plan}).eq("email_hash", key).execute()
            return
        except Exception as e:
            logging.error("update_plan: " + str(e))
    users = _load_users()
    if key in users:
        users[key]["plan"] = plan
        _save_users(users)

def deactivate_user(email: str):
    sb = _sb()
    key = _hash_email(email)
    if sb:
        try:
            sb.table("users").update({"active": False}).eq("email_hash", key).execute()
            return
        except Exception as e:
            logging.error("deactivate_user: " + str(e))
    users = _load_users()
    if key in users:
        users[key]["active"] = False
        _save_users(users)

def get_all_users() -> list:
    sb = _sb()
    if sb:
        try:
            r = sb.table("users").select("*").execute()
            return [_row_to_user(row) for row in (r.data or [])]
        except Exception as e:
            logging.error("get_all_users: " + str(e))
    return list(_load_users().values())

def get_user_count() -> dict:
    all_users = get_all_users()
    total = len(all_users)
    paid = sum(1 for u in all_users if u.get("plan") == "paid")
    active = sum(1 for u in all_users if u.get("active", True))
    return {"total": total, "paid": paid, "free": total - paid, "active": active}
