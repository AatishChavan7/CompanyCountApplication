from celery import shared_task
import csv
from .models import Company

@shared_task
def process_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name, location, industry = row
            Company.objects.create(name=name, location=location, industry=industry)
