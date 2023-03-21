from django.db import models
from main.models import BusTicket
import datetime


# Create your models here.
class monthlySales(models.Model):
    sale_id = models.DateField(db_column="sale_id", primary_key=True)
    daily_sale = models.DecimalField(db_column='daily_sale', blank=True, null=True, max_digits=15, decimal_places=2, default=0)
    used_ticket_qty = models.IntegerField(db_column='used_ticket_qty', blank=True, null=True, default=0)
    used_ticket_amount = models.DecimalField(db_column='used_ticket_amount', blank=True, null=True, max_digits=15, decimal_places=2, default=0)
    pending_ticket_qty = models.IntegerField(db_column='pending_ticket_qty', blank=True, null=True, default=0)
    pending_ticket_amount = models.DecimalField(db_column='pending_ticket_amount', blank=True, null=True, max_digits=15, decimal_places=2, default=0)
    cancel_ticket_qty = models.IntegerField(db_column='cancel_ticket_qty', blank=True, null=True, default=0)
    cancel_ticket_amount = models.DecimalField(db_column='cancel_ticket_amount', blank=True, null=True, max_digits=15, decimal_places=2, default=0)
    total_ticket_qty = models.IntegerField(db_column='total_ticket_qty', blank=True, null=True, default=0)
    refund_ticket_qty = models.IntegerField(db_column='refund_ticket_qty', blank=True, null=True, default=0)
    refund_ticket_amount = models.DecimalField(db_column='refund_ticket_amount', blank=True, null=True, max_digits=15, decimal_places=2, default=0)
    user_qty = models.IntegerField(db_column='user_qty', blank=True, null=True, default=0)

    class Meta:
        db_table = 'monthly_sale'

    def __str__(self):
        sale = str(self.daily_sale)
        return "Daily sale" + sale

