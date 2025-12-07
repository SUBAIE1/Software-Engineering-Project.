


           
import datetime
from hmac import compare_digest
from connection import DatabaseConnection


LOCK_THRESHOLD = 5
LOCK_MINUTES = 15


class AuthResult:
    def __init__(self, ok, reason="", username=None, role_id=None, role=None):
        self.ok = ok
        self.reason = reason
        self.username = username
        self.role_id = role_id
        self.role = role


class AuthService:
    def __init__(self, db=None):
        self.db = db or DatabaseConnection()

    def _fetch_user(self, username):
        query = """
            SELECT  u.username,
                    u.password,
                    u.status,
                    u.failed_attempts,
                    u.locked_until,
                    u.role_id,
                    r.role_name
            FROM users u
            LEFT JOIN roles r ON r.role_id = u.role_id
            WHERE u.username = %s
        """
        return self.db.fetch_one(query, (username,), dictionary=True)

    @staticmethod
    def _is_locked(locked_until):
        return bool(locked_until and locked_until > datetime.datetime.utcnow())

    def _login_successful(self, username):
        self.db.execute_query(
            """
            UPDATE users 
            SET failed_attempts = 0, locked_until = NULL, 
                last_login = CURRENT_TIMESTAMP
            WHERE username = %s
            """,
            (username,)
        )

    def _login_failed(self, username, current_failed):
        new_failed = (current_failed or 0) + 1

        if new_failed >= LOCK_THRESHOLD:
            lock_until = datetime.datetime.utcnow() + datetime.timedelta(minutes=LOCK_MINUTES)
            self.db.execute_query(
                "UPDATE users SET failed_attempts = %s, locked_until = %s WHERE username = %s",
                (new_failed, lock_until, username)
            )
        else:
            self.db.execute_query(
                "UPDATE users SET failed_attempts = %s WHERE username = %s",
                (new_failed, username)
            )

    def validate_credentials(self, username, password):
        try:
            user = self._fetch_user(username)
            print(f"DEBUG: user type: {type(user)}, user value: {user}")

            if not user:
                return AuthResult(False, "USERNAME NOT FOUND")

            if user.get("status") != "ACTIVE":
                return AuthResult(False, "INACTIVE")

            if self._is_locked(user.get("locked_until")):
                return AuthResult(False, "LOCKED")

            stored_password = user.get("password")

            if stored_password and compare_digest(str(password), str(stored_password)):
                self._login_successful(username)
                return AuthResult(
                    True, "OK",
                    username=username,
                    role_id=user["role_id"],
                    role=user["role_name"]
                )

            self._login_failed(username, user.get("failed_attempts"))
            return AuthResult(False, "INVALID")

        except Exception as exc:
            return AuthResult(False, f"SERVICE_ERROR: {exc!r}")
