#!/bin/bash
# Export all the environment variables
export $(grep -v '^#' .env | xargs)

# Start the gunicorn service
gunicorn --bind 0.0.0.0:5000 server:app