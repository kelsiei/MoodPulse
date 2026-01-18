"""Database models for MoodPulse."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MoodEntry(db.Model):
    """Model for storing mood check-ins."""
    __tablename__ = 'mood_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    mood = db.Column(db.String(50), nullable=False)
    intensity = db.Column(db.Integer, nullable=False, default=5)  # 1-10 scale
    context_tags = db.Column(db.String(500))  # Comma-separated tags
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MoodEntry {self.id}: {self.mood} at {self.timestamp}>'
    
    def to_dict(self):
        """Convert mood entry to dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'mood': self.mood,
            'intensity': self.intensity,
            'context_tags': self.context_tags.split(',') if self.context_tags else [],
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
    
    @property
    def tags_list(self):
        """Get context tags as a list."""
        return [tag.strip() for tag in self.context_tags.split(',') if tag.strip()] if self.context_tags else []
