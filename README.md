# MoodPulse
MoodPulse enables quick mood check-ins with contextual tags and transforms them into clear reports that help users understand patterns and optionally share how they feel with trusted people.

# MoodPulse  
*A Human Interaction–Centered Mood Awareness App*

---

## Inspiration
Emotions shift constantly throughout the day—often influenced by people, conversations, and environments. Yet most of us only reflect on our feelings in hindsight, missing patterns that could help us communicate better and take care of ourselves.

**MoodPulse** was built to make emotional patterns visible in real time and transform them into insights that strengthen human connection.

---

## What It Does
MoodPulse allows users to:
- Log their mood in **one tap** at lightweight intervals  
- Add quick **context tags** (alone, friends, online, in-person, etc.)  
- View **daily heatmaps** and **weekly trend reports**  
- Generate **shareable mood snapshots** for trusted people  
- Receive **data-driven micro-insights** based on their own patterns  

No public feeds. No social pressure. Privacy first.

---

## Theme Alignment — *Human Interaction*
MoodPulse enhances human interaction by:
- Helping users understand how **social contexts affect mood**
- Supporting **clear, consent-based emotional communication**
- Encouraging reflection without judgment or “streak pressure”

---

## Information System Design
MoodPulse is designed as a complete **Information System**.

### System Components
- **People:** Users, trusted contacts (optional)
- **Data:** Mood entries, timestamps, context tags, reports
- **Software:** Web/mobile frontend, backend API, database
- **Hardware:** Smartphones, laptops, notification services
- **Procedures:** Check-ins, report generation, consent-based sharing

### Input → Process → Output → Feedback
| Stage | Description |
|-----|-------------|
| Input | 1-tap mood check-in + optional context |
| Process | Aggregation, trend analysis, correlations |
| Output | Heatmaps, weekly summaries, snapshot cards |
| Feedback | Adaptive reminders + personalized insights |

---

## System Development Life Cycle (SDLC)

### 1. Analysis
- Identify emotional awareness + communication gap
- Define success: fast input, useful insights, user trust

### 2. Design
- UX wireframes (check-in & dashboard)
- Data models and system architecture

### 3. Development
- Core logging, analytics, reporting, and sharing features

### 4. Testing
- Requirement-based testing via RTM
- Manual validation of core user flows

### 5. Deployment
- Demo-ready web app
- Public GitHub repository
- Devpost submission + demo video

---

## Requirements

### Functional Requirements
- Log mood in ≤2 taps  
- Tag social/environment context  
- Schedule adaptive check-in reminders  
- View daily & weekly mood reports  
- Share consent-based mood snapshots  

### Nonfunctional Requirements
- Privacy-first (local or encrypted storage)
- Fast dashboard loading (<2s)
- Skip-friendly UX (no streak punishment)
- Responsive across devices

---

## Data Model (MVP)

```text
User
 └── user_id
 └── timezone
 └── notification_window
 └── preferences

MoodEntry
 └── entry_id
 └── user_id
 └── timestamp
 └── mood_value
 └── context_tags
 └── optional_note

Snapshot
 └── snapshot_id
 └── summary_stats
 └── expires_at
 └── permission_scope
