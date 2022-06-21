from django.db import models
from merchants.models import Merchant
from shoppers.models import Shopper

class Order(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    merchant_id = models.ForeignKey(Merchant, on_delete=models.PROTECT)
    shopper_id = models.ForeignKey(Shopper, on_delete=models.PROTECT)
    # Using CharFields to avoid issues with MongoDB (chosen to develop quickly) and because the CSV data is not Timezone-aware
    amount = models.CharField(max_length=16)
    created_at = models.CharField(max_length=20)
    completed_at = models.CharField(max_length=20)
    disembursed = models.BooleanField(default=False)
    