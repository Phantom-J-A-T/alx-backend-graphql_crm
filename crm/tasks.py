import os
import requests
from datetime import datetime  # Added as requested
from celery import shared_task

@shared_task
def generate_crm_report():
    # Define the GraphQL Query
    # Note: Ensure your GraphQL schema has these fields defined
    query = """
    query {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """
    url = 'http://localhost:8000/graphql/' 
    
    try:
        # Executing the GraphQL request
        response = requests.post(url, json={'query': query})
        response.raise_for_status()
        data = response.json().get('data', {})
        
        customers = data.get('totalCustomers', 0)
        orders = data.get('totalOrders', 0)
        revenue = data.get('totalRevenue', 0.0)

        # Formatting the log entry using standard datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

        # Ensure the log file is updated
        log_file_path = '/tmp/crm_report_log.txt'
        with open(log_file_path, 'a') as f:
            f.write(log_entry)
            
    except Exception as e:
        # It's helpful to log errors to the console for Celery worker visibility
        print(f"Error generating report: {e}")