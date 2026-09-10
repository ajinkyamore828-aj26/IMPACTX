
def handle_api_request(route):
    if route == "/api/status":
        return {"status": "ok", "version": "3.2"}
    return {"error": "not found"}
