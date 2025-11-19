# data/fake_messages.py
from __future__ import annotations
import random
import pandas as pd
from datetime import datetime, timedelta

CONTACTS = [
    {"name": "Jim", "avatar": None},
    {"name": "John", "avatar": None},
    {"name": "Barb", "avatar": None},
    {"name": "Alice", "avatar": None},
    {"name": "Sara", "avatar": None},
    {"name": "Mike", "avatar": None},
]

MESSAGE_TEMPLATES = [
    "Hi, I wanted to discuss the transport idea further.",
    "Can you send me the latest document?",
    "Let's meet tomorrow to review your AI proposal.",
    "Thanks for your feedback on the energy project!",
    "Are you available for a call this week?",
    "Here's the updated file for your review.",
    "Great work on the research summary.",
    "Can you clarify the requirements for the next sprint?",
    "Looking forward to collaborating!",
    "Please check the attached report.",
]

RESPONSE_TEMPLATES = [
    "Sounds good, thanks!",
    "Let me check and get back to you.",
    "That makes sense.",
    "I'll update you soon.",
    "Can we discuss this later today?",
    "Appreciate the quick reply.",
    "Let’s plan next steps.",
    "I agree with your point.",
    "Thanks for the clarification!",
    "Working on it now.",
]

USER_RESPONSES = [
    "Sure, thanks for your message!",
    "No problem — I'll take a look.",
    "Good idea, I’ll prepare something.",
    "Happy to discuss further!",
    "Got it, I’ll follow up soon.",
    "I appreciate the update.",
    "Thanks! I'll review it.",
    "Sounds great!",
]

SUBJECTS = [
    "Transport - Helping cities...",
    "AI - Applying 3i algorithms...",
    "Energy- Research in renewables...",
    "Health - Remote patient monitoring...",
    "Education - Personalized learning...",
]

CATEGORIES = ["TRANSPORT", "HEALTH", "ENERGY", "AI", "EDUCATION"]

def generate_thread(contact_name, start_time):
    """Generate a short conversation thread between user and a contact."""

    num_messages = random.randint(2, 6)  # 2–6 messages in thread
    messages = []

    # Start with a message from the contact
    subject = random.choice(SUBJECTS)
    category = random.choice(CATEGORIES)
    text = random.choice(MESSAGE_TEMPLATES)

    current_time = start_time

    # First message (contact → user)
    messages.append({
        "sender": contact_name,
        "receiver": "User",
        "category": category,
        "text": text,
        "timestamp": current_time,
        "read": random.choice([True, False]),
    })

    # Generate alternating replies
    sender = "User"
    for i in range(1, num_messages):
        # Add time gap (5–120 minutes)
        current_time += timedelta(minutes=random.randint(5, 120))

        if sender == "User":
            body = random.choice(USER_RESPONSES)
            next_sender = contact_name
        else:
            body = random.choice(RESPONSE_TEMPLATES)
            next_sender = "User"

        messages.append({
            "sender": sender,
            "receiver": contact_name if sender == "User" else "User",
            "category": category if i == 1 else "",
            "text": body,
            "timestamp": current_time,
            "read": True, 
        })

        sender = next_sender

    return messages


def make_fake_contacts(n: int = 5) -> pd.DataFrame:
    """Generate a fake contacts list."""
    contacts = CONTACTS[:n]
    # Assign a subject to each contact
    subjects = SUBJECTS[:]
    random.shuffle(subjects)
    for i, contact in enumerate(contacts):
        contact["subject"] = subjects[i % len(subjects)]
    return pd.DataFrame(contacts)


def make_fake_messages(n: int = 10, contacts: list = None) -> pd.DataFrame:
    """
    Generate fake messages with conversation threads.
    n = number of threads, NOT messages.
    """

    if contacts is None:
        contacts = CONTACTS

    today = datetime.now()
    start = today - timedelta(days=30)

    rows = []
    for _ in range(n):
        contact = random.choice(contacts)
        thread_start = start + timedelta(minutes=random.randint(0, 43200))
        thread_messages = generate_thread(contact["name"], thread_start)
        rows.extend(thread_messages)

    df = pd.DataFrame(rows)
    df.sort_values("timestamp", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

