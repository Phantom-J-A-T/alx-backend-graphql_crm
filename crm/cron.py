from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Optional GraphQL hello query
    try:
        transport = RequestsHTTPTransport(
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


def updatelowstock():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=True
    )

    mutation = gql("""
    mutation {
        updateLowStockProducts {
            success
            products {
                name
                stock
            }
        }
    }
    """)

    try:
        result = client.execute(mutation)
    except Exception:
        return

    with open("/tmp/low_stock_updates_log.txt", "a") as log:
        for product in result["updateLowStockProducts"]["products"]:
            log.write(
                f"{timestamp} - {product['name']} restocked to {product['stock']}\n"
            )