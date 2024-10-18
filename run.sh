#!/bin/sh

# Initialize the database
poetry run python -m src.utils.initialize_db

# Start the FastAPI application
poetry run fastapi run src/main.py
