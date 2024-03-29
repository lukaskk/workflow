from django.core.management.base import BaseCommand
from .models import Order

class Command(BaseCommand):
    help = 'Updates all order records to status complete'

    def handle(self, *args, **kwargs):
        Order.objects.all().update(status='complete')
        self.stdout.write(self.style.SUCCESS('Successfully updated all orders to "complete" status'))
