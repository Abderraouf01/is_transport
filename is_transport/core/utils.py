import uuid

def generate_tracking():
    return f"KMHA-{uuid.uuid4().hex[:10].upper()}"