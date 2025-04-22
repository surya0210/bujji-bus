"""
File: run_server.py
Date: 16 April 2025
Company: Annalect
Primary Authors: Pasumarthi Surya Narayana
"""


import uvicorn

from app.app_definition import bujji_bus_app

if __name__ == "__main__":
    uvicorn.run(bujji_bus_app, host="0.0.0.0", port=8001)
    