
import database
import utils

def render_overview(user):
    print(f"Welcome {user.username} to your Analytics Dashboard.")
    stats = fetch_system_metrics()
    utils.format_date("2026-09-06")
    return stats

def fetch_system_metrics():
    return {"cpu": "12%", "memory": "4.2GB", "uptime": "99.9%"}
