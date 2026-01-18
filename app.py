"""Main application file for MoodPulse."""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from config import Config
from models import db, MoodEntry

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Predefined mood options
MOOD_OPTIONS = ['happy', 'sad', 'anxious', 'calm', 'energetic', 'tired', 'frustrated', 'content']

# Predefined context tags focused on human interaction
CONTEXT_TAGS = [
    'alone', 'with_friends', 'with_family', 'at_work', 'social_event',
    'one_on_one', 'group_setting', 'helping_someone', 'received_support',
    'conflict', 'positive_interaction', 'online_interaction'
]

# Interaction tags for analysis (tags that indicate being with others)
INTERACTION_TAGS = [
    'with_friends', 'with_family', 'social_event', 'one_on_one',
    'group_setting', 'positive_interaction', 'helping_someone', 'received_support'
]

# Configuration constants
DEFAULT_DAYS = 7
DEFAULT_INTENSITY = 5
MAX_SNAPSHOT_CONTEXTS = 5
MAX_RECENT_ENTRIES = 10
MAX_DAYS_QUERY = 365  # Maximum days allowed for queries


def analyze_mood_patterns(days=DEFAULT_DAYS):
    """Analyze mood patterns over specified days."""
    start_date = datetime.utcnow() - timedelta(days=days)
    entries = MoodEntry.query.filter(MoodEntry.timestamp >= start_date).order_by(MoodEntry.timestamp).all()
    
    if not entries:
        return None
    
    # Basic statistics
    moods = [entry.mood for entry in entries]
    intensities = [entry.intensity for entry in entries]
    mood_counts = Counter(moods)
    
    # Context analysis - focus on human interaction patterns
    context_mood_map = defaultdict(list)
    for entry in entries:
        for tag in entry.tags_list:
            context_mood_map[tag].append({
                'mood': entry.mood,
                'intensity': entry.intensity
            })
    
    # Calculate average intensity per context
    context_insights = {}
    for context, mood_data in context_mood_map.items():
        avg_intensity = sum(m['intensity'] for m in mood_data) / len(mood_data)
        mood_dist = Counter(m['mood'] for m in mood_data)
        context_insights[context] = {
            'count': len(mood_data),
            'avg_intensity': round(avg_intensity, 1),
            'mood_distribution': dict(mood_dist)
        }
    
    # Identify patterns around human interactions
    interaction_entries = [e for e in entries if any(tag in e.tags_list for tag in INTERACTION_TAGS)]
    alone_entries = [e for e in entries if 'alone' in e.tags_list]
    
    interaction_avg = sum(e.intensity for e in interaction_entries) / len(interaction_entries) if interaction_entries else 0
    alone_avg = sum(e.intensity for e in alone_entries) / len(alone_entries) if alone_entries else 0
    
    return {
        'total_entries': len(entries),
        'most_common_mood': mood_counts.most_common(1)[0] if mood_counts else ('N/A', 0),
        'avg_intensity': round(sum(intensities) / len(intensities), 1),
        'context_insights': context_insights,
        'interaction_impact': {
            'with_others_avg': round(interaction_avg, 1),
            'alone_avg': round(alone_avg, 1),
            'difference': round(interaction_avg - alone_avg, 1)
        },
        'entries': [entry.to_dict() for entry in entries],
        'recent_entries': [entry.to_dict() for entry in entries[-MAX_RECENT_ENTRIES:]]
    }


def generate_support_snapshot():
    """Generate a shareable support snapshot of recent mood patterns."""
    analysis = analyze_mood_patterns(days=DEFAULT_DAYS)
    
    if not analysis:
        return "No mood data available yet."
    
    snapshot = f"""MoodPulse Support Snapshot (Last 7 Days)

Total Check-ins: {analysis['total_entries']}
Most Common Mood: {analysis['most_common_mood'][0]} ({analysis['most_common_mood'][1]} times)
Average Intensity: {analysis['avg_intensity']}/10

Human Interaction Insights:
- Average mood with others: {analysis['interaction_impact']['with_others_avg']}/10
- Average mood alone: {analysis['interaction_impact']['alone_avg']}/10
- Impact: {'+' if analysis['interaction_impact']['difference'] > 0 else ''}{analysis['interaction_impact']['difference']}

Key Context Patterns:
"""
    
    # Sort contexts by frequency
    sorted_contexts = sorted(analysis['context_insights'].items(), 
                           key=lambda x: x[1]['count'], reverse=True)[:MAX_SNAPSHOT_CONTEXTS]
    
    for context, data in sorted_contexts:
        snapshot += f"- {context}: {data['count']} times, avg intensity {data['avg_intensity']}/10\n"
    
    snapshot += "\nThis snapshot helps trusted people understand my recent mood patterns."
    
    return snapshot


@app.route('/')
def index():
    """Home page with check-in form."""
    return render_template('index.html', moods=MOOD_OPTIONS, contexts=CONTEXT_TAGS)


@app.route('/checkin', methods=['POST'])
def checkin():
    """Create a new mood check-in."""
    data = request.form
    
    mood = data.get('mood')
    
    # Validate mood against allowed options
    if not mood or mood not in MOOD_OPTIONS:
        return jsonify({'error': 'Invalid mood selected'}), 400
    
    # Validate and parse intensity with fallback to default
    try:
        intensity = int(data.get('intensity', DEFAULT_INTENSITY))
        # Ensure intensity is within valid range
        intensity = max(1, min(10, intensity))
    except (ValueError, TypeError):
        intensity = DEFAULT_INTENSITY
    
    # Validate context tags against allowed options
    submitted_tags = data.getlist('context_tags')
    valid_tags = [tag for tag in submitted_tags if tag in CONTEXT_TAGS]
    context_tags = ','.join(valid_tags)
    
    notes = data.get('notes', '')
    
    entry = MoodEntry(
        mood=mood,
        intensity=intensity,
        context_tags=context_tags,
        notes=notes
    )
    
    db.session.add(entry)
    db.session.commit()
    
    return redirect(url_for('index'))


@app.route('/report')
def report():
    """View mood analysis report."""
    days = request.args.get('days', DEFAULT_DAYS, type=int)
    # Validate days parameter to prevent DoS
    days = max(1, min(days, MAX_DAYS_QUERY))
    analysis = analyze_mood_patterns(days=days)
    
    if not analysis:
        return render_template('report.html', no_data=True)
    
    return render_template('report.html', analysis=analysis, days=days)


@app.route('/snapshot')
def snapshot():
    """Generate and display support snapshot."""
    snapshot_text = generate_support_snapshot()
    return render_template('snapshot.html', snapshot=snapshot_text)


@app.route('/api/entries')
def api_entries():
    """API endpoint to get mood entries as JSON."""
    days = request.args.get('days', 30, type=int)
    # Validate days parameter to prevent DoS
    days = max(1, min(days, MAX_DAYS_QUERY))
    start_date = datetime.utcnow() - timedelta(days=days)
    entries = MoodEntry.query.filter(MoodEntry.timestamp >= start_date).order_by(MoodEntry.timestamp.desc()).all()
    
    return jsonify([entry.to_dict() for entry in entries])


@app.route('/api/analysis')
def api_analysis():
    """API endpoint to get mood analysis as JSON."""
    days = request.args.get('days', DEFAULT_DAYS, type=int)
    # Validate days parameter to prevent DoS
    days = max(1, min(days, MAX_DAYS_QUERY))
    analysis = analyze_mood_patterns(days=days)
    
    if not analysis:
        return jsonify({'error': 'No data available'}), 404
    
    return jsonify(analysis)


def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    init_db()
    # Debug mode should be disabled in production for security
    # Enable via environment variable for development: FLASK_DEBUG=1
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    # Use 127.0.0.1 for local development, or set FLASK_HOST for specific needs
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(debug=debug_mode, host=host, port=port)
