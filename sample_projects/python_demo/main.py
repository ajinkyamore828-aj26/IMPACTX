
import auth
import database
import dashboard
import utils

def start_application():
    print("Initializing Enterprise Application...")
    conn = database.connect_db("prod.db")
    user = auth.login("admin@example.com", "secret123")
    if user:
        dashboard.render_overview(user)
    print("Application running.")

if __name__ == "__main__":
    start_application()
