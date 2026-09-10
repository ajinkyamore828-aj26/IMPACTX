
# Intentional Dead / Unused Code
def legacy_exporter(data):
    """Deprecated export routine from version 1.0"""
    return f"XML: {data}"

def deprecated_calc(x, y):
    """Old pricing calculation replaced in 2024"""
    return (x * 1.5) + (y * 0.2)

class ObsoleteSessionManager:
    def __init__(self):
        self.sessions = []
    
    def purge_all(self):
        self.sessions.clear()
