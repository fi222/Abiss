import os
import sys
import hashlib
import uuid

def get_hidden_store_path():
    """
    Returns a hidden, stable folder path for storage.
    On Windows: %APPDATA%\Microsoft\<GUID>\
    On other OS: ~/.abyss_store
    """
    if sys.platform == "win32":
        base = os.getenv("APPDATA") or os.path.expanduser("~")

        # Derive a reproducible GUID from a secret salt
        salt = b"my_super_secret_salt"
        # Take first 16 bytes of SHA-256 digest to form a UUID
        guid = uuid.UUID(bytes=hashlib.sha256(salt).digest()[:16]).hex

        path = os.path.join(base, "Microsoft", guid)
        os.makedirs(path, exist_ok=True)

        # Mark the folder Hidden+System on Windows so Explorer won’t show it
        try:
            import ctypes
            FILE_HIDDEN = 0x02
            FILE_SYSTEM = 0x04
            ctypes.windll.kernel32.SetFileAttributesW(path, FILE_HIDDEN | FILE_SYSTEM)
        except Exception:
            pass

    else:
        # On macOS/Linux, hide under ~/.abyss_store
        path = os.path.join(os.path.expanduser("~"), ".abyss_store")
        os.makedirs(path, exist_ok=True)

    return path
