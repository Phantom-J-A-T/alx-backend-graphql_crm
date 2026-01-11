from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Optional GraphQL hello query
    try:
        transport = RequestsHTTPHTTPTransport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(
            transport=transport,
            fetch_schema_from_transport=True
        )
        query = gql("{ hello }")
        client.execute(query)
    except Exception:
        pass

    with open("/tmp/crm_heartbeat_log.txt", "a") as log:
        log.write(message)