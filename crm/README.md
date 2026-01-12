# CRM Weekly Reporting Setup

### 1. Install Dependencies
Ensure Redis is installed on your system, then install Python packages:
```bash
sudo apt install redis-server
pip install -r requirements.txt

2. Database Migrations
Initialize the tables required for django-celery-beat:

Bash

python manage.py migrate
3. Run the Services
Open three terminal tabs to run the following:

Tab 1: Django Server

Bash

python manage.py runserver
Tab 2: Celery Worker

Bash

celery -A crm worker -l info
Tab 3: Celery Beat (The Scheduler)

Bash

celery -A crm beat -l info
4. Verification
The report is scheduled for Monday at 6:00 AM. To verify it is working immediately, you can trigger the task manually via the Django shell:

Python

from crm.tasks import generate_crm_report
generate_crm_report.delay()
Check the output:

Bash

cat /tmp/crm_report_log.txt