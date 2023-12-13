# config.py
SERVER_ADDRESS = '127.0.0.1'
USERNAME = '20120566@student.hcmus.edu.vn'
PASSWORD = '12102002'
SMTP_PORT = 2225
POP3_PORT = 3335
Autoload = 10

FILTER_RULES = [
    {"type": "from", "addresses": ["sonvo1611@testing.com", "ahuu@testing.com"], "folder": "Test"},
    {"type": "subject", "keywords": ["urgent", "ASAP"], "folder": "Important"},
    {"type": "content", "keywords": ["report", "meeting"], "folder": "Work"},
    {"type": "spam", "keywords": ["virus", "hack", "crack"], "folder": "Spam"},
]
