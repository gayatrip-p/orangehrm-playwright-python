"""
Login test data — keeps test logic separate from test data.
Import INVALID_LOGINS in your test with pytest.mark.parametrize.
"""

# Valid admin credentials (loaded from .env in real runs)
VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"

# Invalid credential combinations for negative tests
INVALID_LOGINS = [
    ("Admin",        "wrongpass",   "Invalid credentials"),
    ("wronguser",    "admin123",    "Invalid credentials"),
    ("wronguser",    "wrongpass",   "Invalid credentials"),
    ("",             "admin123",    "Required"),
    ("Admin",        "",            "Required"),
    ("",             "",            "Required"),
    ("admin",        "admin123",    "Invalid credentials"),  # case-sensitive
    ("ADMIN",        "admin123",    "Invalid credentials"),  # case-sensitive
    (" Admin",       "admin123",    "Invalid credentials"),  # leading space
    ("Admin",        "admin123 ",   "Invalid credentials"),  # trailing space
]

# Expected messages
EXPECTED_ERROR_MSG   = "Invalid credentials"
EXPECTED_REQUIRED    = "Required"
DASHBOARD_URL_FRAG   = "/dashboard"
LOGIN_PAGE_TITLE     = "Login"
