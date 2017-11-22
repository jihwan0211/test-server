"""
API CONFIG
"""

import os

DEBUG = False
if os.getenv("DEBUG", "ON") == "ON":
    DEBUG = True

OK = {"message":"ok"}
BAD_REQUEST = {"message":"wrong param"}
FAILURE = {"message":"failure"}
NOT_MODIFIED = {"message":"not modified"}
UNAUTHORIZED = {"message":"unauthorized"}
UNKNOWN_ERROR = {"message":"server interval error"}