import csv
from django.core.management.base import BaseCommand
from company.models import Company

class Command(BaseCommand):
    help = 'Imports company data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be imported')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Company.objects.create(
                    id=row['id'],
                    name=row['name'],
                    domain=row['domain'],
                    year_founded=int(row['year founded']) if row['year founded'] else None,
                    industry=row['industry'],
                    size_range=row['size range'],
                    locality=row['locality'],
                    country=row['country'],
                    linkedin_url=row['linkedin url'],
                    current_employee_estimate=int(row['current employee estimate']),
                    total_employee_estimate=int(row['total employee estimate'])
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported data'))