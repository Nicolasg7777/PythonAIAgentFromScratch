# AI Customer Support Agent

A Python-based AI customer support chatbot that demonstrates core data engineering and software development concepts. Built as a personal learning project to practice skills relevant to Analytics Data Engineering roles.

## Purpose

This project was built from scratch as a hands-on exercise to understand and practice:

- **Data Modeling & SQL** - Relational database design with foreign keys
- **ETL Concepts** - Extract, Transform, Load data pipelines
- **API Integration** - REST API calls to AI and email services
- **Regex Data Extraction** - Pattern matching for unstructured text
- **Batch Processing** - Automated scheduled jobs
- **Error Handling** - Fault tolerance with fallback mechanisms

## Project Structure

```
PythonAIAgentFromScratch/
├── config.py          # Centralized configuration and API keys
├── database.py        # SQLite database operations and schema
├── ai_chat.py         # Groq API integration for AI responses
├── extractor.py       # Regex patterns for data extraction
├── email_sender.py    # Resend API for email notifications
├── main.py            # Main chat loop orchestration
├── reminder_job.py    # Automated reminder batch processing
└── README.md
```

## Database Schema

```
PROFILES (1) ──────< (Many) SESSIONS
                          │
                          └────< (Many) MESSAGES

PROFILES (1) ──────< (Many) BOOKINGS
SESSIONS (1) ──────< (Many) BOOKINGS
```

**Tables:**
- `profiles` - Customer contact information
- `sessions` - Chat conversation sessions
- `messages` - Individual chat messages
- `bookings` - Scheduled consultations

## Key Concepts Demonstrated

### 1. Data Modeling
- One-to-many relationships with foreign keys
- CHECK constraints for data validation
- AUTOINCREMENT primary keys

### 2. ETL Pipeline
- **Extract**: User input from chat, data from APIs
- **Transform**: Regex extraction of emails, phones, names
- **Load**: Structured data saved to SQLite database

### 3. API Integration
- Groq API for LLM-powered responses
- Resend API for transactional emails
- Error handling with model fallbacks

### 4. Automation
- Batch processing for reminder emails
- Scheduled job pattern for daily tasks

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nicolasg7777/PythonAIAgentFromScratch.git
   cd PythonAIAgentFromScratch
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install requests
   ```

4. **Get API Keys (Free)**
   - Groq API: https://console.groq.com
   - Resend API: https://resend.com (optional, for emails)

5. **Update config.py**
   ```python
   GROQ_API_KEY = "your_actual_key_here"
   ```

6. **Run the chatbot**
   ```bash
   python main.py
   ```

## Usage Example

```
==================================================
AI Customer Support Agent
Type 'quit' to exit.
==================================================

Database initialized successfully.
[Session 1 started]

You: Hello
Bot: Welcome! My name is HealthBot. How can I help you today?

You: I'd like to schedule a consultation
Bot: I'd be happy to help. Could you please provide your name and email?

You: Bob Garcia is my name, email is bob@example.com
Bot: Thank you, Bob. I've noted your information...

You: quit

Analyzing conversation for contact information...
Extracted: {'email': 'bob@example.com', 'phone': None, 'name': 'Bob Garcia'}
Profile saved! ID: 1
```

## Skills Practiced

| Component | Skills |
|-----------|--------|
| `database.py` | SQL, Data Modeling, CRUD Operations, JOINs |
| `ai_chat.py` | REST APIs, JSON, Error Handling |
| `extractor.py` | Regex, Pattern Matching, Data Transformation |
| `email_sender.py` | External API Integration |
| `main.py` | Orchestration, Control Flow |
| `reminder_job.py` | Batch Processing, Automation |

## Technologies Used

- **Python 3.12**
- **SQLite** - Lightweight relational database
- **Groq API** - Fast LLM inference (Llama models)
- **Resend API** - Transactional email service
- **Regex** - Pattern matching for data extraction

## Future Improvements

- [ ] Add unit tests for each module
- [ ] Implement environment variables for API keys
- [ ] Add more robust phone number regex patterns
- [ ] Create a web interface with Flask/FastAPI
- [ ] Add conversation analytics dashboard

## Author

**Nicolas Garcia**
Personal learning project for Analytics Data Engineering skills development.

## License

This project is for educational purposes.
