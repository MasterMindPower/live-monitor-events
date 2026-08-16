import os
import sys
from cryptography.fernet import Fernet, InvalidToken

ENC_FILE = "simple.enc"


def main():
    decrypt_key = os.environ.get("DECRYPT_KEY")

    if not decrypt_key:
        print("Error: DECRYPT_KEY environment variable is not set.", file=sys.stderr)
        print("Please set DECRYPT_KEY in your GitHub Secrets or environment.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(ENC_FILE):
        print(f"Error: Encrypted payload file '{ENC_FILE}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        fernet = Fernet(decrypt_key.encode("utf-8") if isinstance(decrypt_key, str) else decrypt_key)
        with open(ENC_FILE, "rb") as f:
            encrypted_data = f.read()

        decrypted_code = fernet.decrypt(encrypted_data).decode("utf-8")
    except InvalidToken:
        print("Error: Invalid DECRYPT_KEY. Decryption failed.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during decryption: {e}", file=sys.stderr)
        sys.exit(1)

    # Execute the decrypted script in-memory
    exec_globals = {
        "__name__": "__main__",
        "__file__": "simple.py",
        "__builtins__": __builtins__,
    }
    try:
        exec(decrypted_code, exec_globals)
    except Exception as e:
        print(f"Error executing payload: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
