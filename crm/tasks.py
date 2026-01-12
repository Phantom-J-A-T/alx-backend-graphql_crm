import os
import requests
from celery import shared_task
from django.utils import timezone

@shared_task
def generate_crm_report():
    # Define the GraphQL Query
    query = """
    query {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """
    url = 'http://localhost:8000/graphql/' # Update if your endpoint differs
    
    try:
        response = requests.post(url, json={'query': query})
        data = response.json()['data']
        
        customers = data.get('totalCustomers', 0)
        orders = data.get('totalOrders', 0)
        revenue = data.get('totalRevenue', 0.0)

        # Formatting the log entry
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

        # Write to log file
        log_file_path = '/tmp/crm_report_log.txt'
        with open(log_file_path, 'a') as f:
            f.write(log_entry)
            
    except Exception as e:
        print(f"Error generating report: {e}")