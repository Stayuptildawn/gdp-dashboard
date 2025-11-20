# generate_initial_data.py
import random
import pandas as pd
from datetime import date, timedelta
import os


STATUSES = ["On Review", "Accepted", "Rejected"]


def _rand_date(start: date, end: date) -> date:
    """Pick a random date between start and end"""
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def generate_initial_ideas(n: int = 50):
    """Generate fake ideas and save to CSV"""
    today = date.today()
    start = today - timedelta(days=120)

    # List of possible owners (users)
    owners = ["admin", "user1", "user2", "user3", "user4"]

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
            "Collaborative idea board for innovation teams.",
            "Virtual reality platform for remote laboratory work.",
            "Blockchain supply chain tracker for sustainable products.",
            "Automated code review tool using machine learning.",
            "Smart parking system with real-time availability updates.",
            "AI-powered mental health support chatbot.",
            "Waste management optimizer using IoT sensors.",
            "3D printing marketplace for custom medical devices.",
            "Automated scientific literature search engine.",
            "Real-time wildfire detection using satellite imagery.",
            "Smart irrigation system for agricultural optimization.",
            "Virtual career counseling platform with AI guidance.",
            "Automated accessibility checker for web applications.",
            "Carbon footprint calculator for supply chains.",
            "AI-based news fact-checking tool.",
            "Predictive model for student dropout prevention.",
            "Smart building energy management system.",
            "Automated grant matching service for researchers.",
            "Voice-controlled lab equipment interface.",
            "Collaborative research paper annotation tool.",
            "AI-powered drug discovery acceleration platform."
        ]
        description = desc_templates[(i-1) % len(desc_templates)]
        
        # Assign owner - make every 3rd idea belong to 'admin' for testing
        owner = "admin" if i % 3 == 0 else random.choice(owners[1:])
        
        rows.append({
            "id": i,
            "Status": random.choices(STATUSES, weights=[5, 3, 2])[0],  # Mix of statuses
            "From date": fd,
            "To date": td,
            "Document name": f"PROFORMA/{pub.strftime('%d/%m/%Y')}",
            "Date published": pub,
            "Issue Number": f"{random.randint(100,999)}.{random.randint(10,99)}/{random.randint(100,999)}PLN",
            "Name": f"Project {i}: {desc_templates[(i-1) % len(desc_templates)].split()[0]} Innovation",
            "Category": random.choice(["TRANSPORT", "HEALTH", "ENERGY", "AI", "Technology", "Social"]),
            "Description": description,
            "Detailed Description": "Integer rutrum, odio at scelerisque fermentum, purus libero mattis mi, sed tristique mauris sapien eu tortor. Donec accumsan, urna vel bibendum faucibus, lorem nisi consequat justo, vitae venenatis eros magna id ex.",
            "Estimated Impact / Target Audience": random.choice([
                "Students, Researchers, Academic institutions",
                "SMEs, Startups, Tech companies",
                "City residents, Urban planners, Government",
                "Healthcare providers, Patients, Medical staff",
                "Engineers, Industrial facilities, Manufacturing"
            ]),
            "Owner": owner
        })
    
    df = pd.DataFrame(rows)
    # Sort so newer ideas appear first
    df.sort_values(["Date published"], ascending=[False], inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save to CSV
    csv_path = "data/ideas.csv"
    df.to_csv(csv_path, index=False)
    
    print(f"✅ Successfully generated {n} ideas!")
    print(f"📁 Saved to: {csv_path}")
    print(f"\nBreakdown:")
    print(f"  - Admin's ideas: {len(df[df['Owner'] == 'admin'])}")
    print(f"  - Other users: {len(df[df['Owner'] != 'admin'])}")
    print(f"\nStatus distribution:")
    print(df['Status'].value_counts())
    print(f"\nCategory distribution:")
    print(df['Category'].value_counts())
    
    return df


if __name__ == "__main__":
    generate_initial_ideas(50)
