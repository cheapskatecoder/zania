import os
from zania.settings.base import *


SECRET_KEY = "3a5q7&5n_7)ljdyen8c=24qyr1s2u*3x58ht=yir)f$yv$3z6_4t642m=b)f^8lw1ac*f-f2)wae!lgq*n1m#9jha-&v5a45k=0p"

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
