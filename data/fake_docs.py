# data/fake_docs.py
from __future__ import annotations
import random
import pandas as pd
from datetime import date, timedelta


STATUSES = ["On Review", "Accepted", "Rejected"]


def _rand_date(start: date, end: date) -> date:
    """Pick a random date between start and end"""
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def make_fake_docs(n: int = 30) -> pd.DataFrame:
    """Generate some fake document data for testing/demo purposes"""
    today = date.today()
    start = today - timedelta(days=120)


    rows = []
    for i in range(1, n + 1):
        # Create random dates that make sense (from -> to -> published)
        fd = _rand_date(start, today - timedelta(days=1))
        td = _rand_date(fd, fd + timedelta(days=14))
        pub = _rand_date(fd, td)
        # Generate a unique description for each idea
        desc_templates = [
            "AI assistant for monitoring research progress and suggesting funding opportunities.",
            "Machine learning model for predicting traffic congestion in smart cities.",
            "AI-driven tool for automating document classification and tagging.",
            "Renewable energy optimizer for reducing waste in solar grid systems.",
            "Chatbot platform for academic support and student engagement.",
            "Computer vision tool for detecting anomalies in industrial processes.",
            "Smart energy meter analyzing consumption patterns using AI.",
            "Natural language model that summarizes technical research papers.",
            "AI-powered emotion recognition for improving user experience design.",
            "Sustainable transport model integrating electric mobility data.",
            "Blockchain-based credential verification for academic records.",
            "Predictive analytics for hospital resource management.",
            "IoT platform for real-time air quality monitoring.",
            "Personalized learning recommendation engine for online education.",
            "Remote patient monitoring system using wearable devices.",
            "Crowdsourced mapping tool for disaster response coordination.",
            "AI-based plagiarism detection for research publications.",
            "Automated grant application reviewer using NLP.",
            "Energy consumption dashboard for smart homes.",
            "Digital twin simulation for urban planning.",
            "AI-powered literature review assistant.",
            "Speech-to-text tool for academic interviews.",
            "Open data portal for city infrastructure projects.",
            "Real-time translation tool for international collaboration.",
            "AI-based reviewer assignment for journals.",
            "Predictive maintenance for laboratory equipment.",
            "Research impact visualization dashboard.",
            "Automated scheduling assistant for research teams.",
            "Data anonymization tool for sensitive research datasets.",
            "Collaborative idea board for innovation teams."
        ]
        description = desc_templates[(i-1) % len(desc_templates)]
        rows.append({
            "id": 1600 + i,
            "Status": random.choices(STATUSES, weights=[0, 1, 0])[0],  # Bias toward "On Review"
            "From date": fd,
            "To date": td,
            "Document name": f"PROFORMA/{pub.strftime('%d/%m/%Y')}",
            "Date published": pub,
            "Issue Number": f"{random.randint(100,999)}.{random.randint(10,99)}/{random.randint(100,999)}PLN",
            "Name": f"Project {i}",
            "Category": random.choice(["TRANSPORT", "HEALTH", "ENERGY", "AI"]),
            "Description": description,
            "Detailed Description": "Integer rutrum, odio at scelerisque fermentum, purus libero mattis mi, sed tristique mauris sapien eu tortor.",
            "Estimated Impact / Target Audience": "Vestibulum non nibh a arcu sodales aliquam nec vel magna."
        })
    df = pd.DataFrame(rows)
    # Sort so "Accepted" and "On Review" show up first, newest dates on top
    df.sort_values(["Status", "From date"], ascending=[True, False], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
