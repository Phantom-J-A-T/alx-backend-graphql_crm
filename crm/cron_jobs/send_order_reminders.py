#!/usr/bin/python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL client setup
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
query GetRecentOrders($since: DateTime!) {
  orders(orderDate_Gte: $since) {
    id
    customer {
      email
    }
  }
}
""")

since_date = (datetime.now() - timedelta(days=7)).isoformat()

result = client.execute(query, variable_values={"since": since_date})

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("/tmp/orderreminderslog.txt", "a") as log:
    for order in result.get("orders", []):
        log.write(
            f"{timestamp} - Order ID: {order['id']}, "
            f"Customer Email: {order['customer']['email']}\n"
        )

print("Order reminders processed!")