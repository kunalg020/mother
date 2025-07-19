# dhan_config.py

# Secure version: fetch credentials from environment variables
import os

DHAN_API_KEY = os.getenv("DHAN_API_KEY")
DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
