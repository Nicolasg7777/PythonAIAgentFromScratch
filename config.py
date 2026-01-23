'''
    Configuration settings for AI Agent
    Why a seperate file>

    1. Security: API keys in one place.
    2. Maintainability: change once, affects everywhere.
    3. Environment switching: dev vs prod settings.
'''

# Databse Configuration
DATABASE_NAME = "ai_agent.db" # SQLite creates this file automatically.

# Groq API (for AI chat) - Free tier available at consolegroq.com
GROQ_API_KEY = "your_groq_api_key_here"  # Get free key at console.groq.com
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions" # Groq API endpoint for chat completions.

# AI Model - Groq offers free access to these Llama models.
AI_MODEL = "llama-3.1-8b-instant" # fast and free.
AI_MODEL_FALLBACK = "llama-3.1-70b-versatile" # Backup if it first fails.

# Resend API (for emails) - Free tier at resend.com
RESEND_API_KEY = "your_resend_api_key" # We can get this later.
RESEND_API_URL = "https://api.resend.com/emails" 
FROM_EMAIL = "onboarding@resend.com" # Free Tier uses this.

# Agent name
AGENT_NAME = "HealthBot"

# System prompt - this tells the AI how to behave.
SYSTEM_PROMPT = f""" You are a helpful customer support agent named {AGENT_NAME} for a healthcare company.
Your goals:
1. Answer questions about services.
2. Collect contact information ( name, email, phone).
3. Help Schedule consultations.
Be professional, friendly, and HIPAA-conscious - never ask for medical details."""

