# data/fake_docs.py
from __future__ import annotations
import random
import pandas as pd
from datetime import date, timedelta

STATUSES = ["On Review", "Accepted", "Rejected"]

def _rand_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def make_fake_docs(n: int = 30) -> pd.DataFrame:
    today = date.today()
    start = today - timedelta(days=120)

    rows = []
    for i in range(1, n + 1):
        fd = _rand_date(start, today - timedelta(days=1))
        td = _rand_date(fd, fd + timedelta(days=14))
        pub = _rand_date(fd, td)
        rows.append({
            "id": 1600 + i,
            "Status": random.choices(STATUSES, weights=[0.5, 0.35, 0.15])[0],
            "From date": fd,
            "To date": td,
            "Document name": f"PROFORMA/{pub.strftime('%d/%m/%Y')}",
            "Date published": pub,
            "Issue Number": f"{random.randint(100,999)}.{random.randint(10,99)}/{random.randint(100,999)}PLN",
            "Name": f"Project {i}",
            "Category": random.choice(["TRANSPORT", "HEALTH", "ENERGY", "AI"]),
            "Description": f"Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Detailed Description": f"Integer rutrum, odio at scelerisque fermentum, purus libero mattis mi, sed tristique mauris sapien eu tortor.",
            "Estimated Impact / Target Audience": f"Vestibulum non nibh a arcu sodales aliquam nec vel magna."
        })
    df = pd.DataFrame(rows)
    df.sort_values(["Status", "From date"], ascending=[True, False], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
