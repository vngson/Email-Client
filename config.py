# config.py
SERVER_ADDRESS = '127.0.0.1'
USERNAME = 'your_email'
PASSWORD = 'your_password'
SMTP_PORT = 2225
POP3_PORT = 3335
Autoload = 1000

FILTER_RULES = [
    {"type": "from", "addresses": ["test@gmail.com"], "folder": "Test"},
    {"type": "to", "addresses": ["test@gmail.com", "your_email"], "folder": "Test"},
    {"type": "subject", "keywords": ["urgent", "ASAP"], "folder": "Important"},
    {"type": "content", "keywords": ["report", "meeting"], "folder": "Work"},
    {"type": "spam", "keywords": ["spam", "virus", "hack", "crack"], "folder": "Spam"},
]

DEFAULT_FOLDER = "Inbox"