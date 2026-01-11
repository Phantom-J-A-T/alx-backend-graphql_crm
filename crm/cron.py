from datetime import datetime
import requests

def logcrmheartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Optional GraphQL hello query
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=3
        )
    except Exception:
        pass

    with open("/tmp/crmheartbeatlog.txt", "a") as log:
        log.write(message)