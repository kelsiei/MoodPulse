# MoodPulse 🌊

**Track mood + context in lightweight check-ins and generate reports that help people understand patterns and communicate needs.**

## Purpose

MoodPulse helps you understand how your moods shift around human interactions through:
- 📝 **Quick mood check-ins** with context tags
- 📊 **Pattern analysis** highlighting interaction impacts
- 🤝 **Support snapshots** for sharing with trusted people (consent-based)

## Features

### 1. Mood Check-ins
- Select from 8 mood options (happy, sad, anxious, calm, energetic, tired, frustrated, content)
- Rate intensity on a 1-10 scale
- Tag context with focus on human interactions:
  - Social contexts: alone, with_friends, with_family, social_event
  - Interaction types: one_on_one, group_setting, online_interaction
  - Support: helping_someone, received_support, positive_interaction
  - Work context: at_work
  - Conflict situations
- Add optional notes

### 2. Pattern Reports
- View mood trends over 7, 14, or 30 days
- **Human Interaction Insights**: See how your mood differs when with others vs. alone
- **Context Patterns**: Understand which contexts correlate with different moods
- Recent check-ins timeline

### 3. Support Snapshots
- Generate shareable summaries of recent mood patterns
- Privacy-focused: only includes aggregated patterns, not personal notes
- Copy to clipboard for easy sharing
- Helps trusted people understand your emotional landscape

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kelsiei/MoodPulse.git
   cd MoodPulse
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the app:**
   Open your browser and navigate to `http://localhost:5000`

### Development Mode

To enable debug mode for development (not recommended for production):
```bash
FLASK_DEBUG=1 python app.py
```

### Configuration Options

The application can be configured using environment variables:

- `FLASK_DEBUG=1` - Enable debug mode (development only)
- `FLASK_HOST=0.0.0.0` - Bind to all interfaces (use `127.0.0.1` for local only)
- `FLASK_PORT=8080` - Change the port (default: 5000)
- `SECRET_KEY=your-secret-key` - Set secret key for production
- `DATABASE_URL=sqlite:///path/to/db.db` - Custom database location

Example for production:
```bash
SECRET_KEY=your-secure-random-key FLASK_HOST=127.0.0.1 python app.py
```

## Usage

### Creating a Check-in
1. Go to the home page
2. Select your current mood
3. Adjust the intensity slider (1-10)
4. Select relevant context tags (especially around human interactions)
5. Optionally add notes
6. Click "Save Check-in"

### Viewing Reports
1. Click "Reports" in the navigation
2. Choose a time range (7, 14, or 30 days)
3. Review:
   - Overall mood statistics
   - Human interaction impact analysis
   - Context pattern breakdowns
   - Recent check-in timeline

### Sharing a Support Snapshot
1. Click "Share Snapshot" in the navigation
2. Review the generated summary
3. Click "Copy to Clipboard"
4. Share with trusted people who you want to understand your patterns

**Note**: The clipboard feature requires HTTPS or localhost. If the copy button doesn't work, manually select and copy the text from the snapshot box.

## API Endpoints

### GET `/api/entries?days=30`
Returns all mood entries from the specified number of days as JSON.

**Example Response:**
```json
[
  {
    "id": 1,
    "timestamp": "2026-01-18T01:00:00",
    "mood": "happy",
    "intensity": 8,
    "context_tags": ["with_friends", "social_event"],
    "notes": "Great dinner with friends",
    "created_at": "2026-01-18T01:00:00"
  }
]
```

### GET `/api/analysis?days=7`
Returns mood pattern analysis for the specified number of days.

**Example Response:**
```json
{
  "total_entries": 15,
  "most_common_mood": ["happy", 6],
  "avg_intensity": 7.2,
  "interaction_impact": {
    "with_others_avg": 7.8,
    "alone_avg": 6.5,
    "difference": 1.3
  },
  "context_insights": {
    "with_friends": {
      "count": 5,
      "avg_intensity": 8.2,
      "mood_distribution": {"happy": 4, "energetic": 1}
    }
  }
}
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, vanilla JavaScript
- **Date handling**: python-dateutil

## Project Structure

```
MoodPulse/
├── app.py                 # Main application with routes and analysis logic
├── models.py              # Database models (MoodEntry)
├── config.py              # Application configuration
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Check-in form
│   ├── report.html       # Analytics and reports
│   └── snapshot.html     # Support snapshot sharing
└── README.md             # This file
```

## Human Interaction Theme

MoodPulse specifically addresses the "Human Interaction" theme by:

1. **Context tags focused on interactions**: Many tags specifically capture social contexts (alone, with_friends, with_family, social_event, one_on_one, group_setting)

2. **Interaction impact analysis**: Reports automatically calculate and highlight how your mood differs when you're with others vs. alone

3. **Support snapshots**: Enable consent-based sharing of mood patterns with trusted people, facilitating better understanding and support

4. **Pattern recognition**: Helps users notice how their moods shift around different types of human interactions

## Privacy & Data

- All data is stored locally in a SQLite database (`moodpulse.db`)
- No data is sent to external servers
- Support snapshots are generated on-demand and only shared with explicit user action
- Individual notes are never included in snapshots

## Security

MoodPulse implements several security best practices:

- **Input Validation**: All user inputs (mood, intensity, context tags) are validated against allowed values
- **Query Protection**: API parameters are validated to prevent DoS attacks (max 365 days)
- **Secure Secrets**: Secret keys are auto-generated using cryptographically secure methods
- **Debug Mode**: Disabled by default, only enabled via explicit environment variable
- **Host Binding**: Defaults to localhost (127.0.0.1) for security
- **XSS Protection**: Jinja2 auto-escaping enabled for all templates
- **CodeQL Verified**: All code passes GitHub's security analysis

For production deployment:
1. Always set a secure `SECRET_KEY` environment variable
2. Use HTTPS/TLS for network traffic
3. Keep `FLASK_DEBUG` disabled
4. Consider adding authentication for multi-user scenarios

## Future Enhancements

Potential features for future development:
- Multi-user support with authentication
- Data export (CSV, JSON)
- Visualizations (charts and graphs)
- Mood predictions based on patterns
- Reminders for regular check-ins
- Mobile-responsive design improvements
- Dark mode

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available for educational and personal use.
