"""Configuration for MoodPulse application."""
import os
import secrets

class Config:
    """Base configuration."""
    # Generate a random secret key if not provided (for development only)
    # In production, always set SECRET_KEY environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///moodpulse.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

