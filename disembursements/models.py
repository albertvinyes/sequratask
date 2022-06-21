from django.db import models
from datetime import datetime

from merchants.models import Merchant
from orders.models import Order

class Disembursement(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)

    fee_factor = models.DecimalField(max_digits=10, decimal_places=4)
    total_amount = models.DecimalField(max_digits=16, decimal_places=2)
    created_at = models.CharField(max_length=20)

class DisembursementController():

    MAX_FEE_FACTOR = 1.0100
    MED_FEE_FACTOR = 1.0095
    MIN_FEE_FACTOR = 1.0085

    # Applies necessary fee to the amount.
    # param amount is a float number
    # returns an array with the increased amount and the fee factor
    @classmethod
    def apply_fee(self, amount):
        # Setup fee multiplier.
        if amount < 50:
            f = self.MAX_FEE_FACTOR
        elif amount < 300:
            f = self.MED_FEE_FACTOR
        else:
            f = self.MIN_FEE_FACTOR
        return [amount, f]

    # Creates a disembursement
    # param order is an Order object
    # returns the new total amount
    @classmethod
    def create_disemburse(self, order):
        # Casting required in amount due to how the databe treats the amount field.
        amount = float(str(order['amount']))

        # IDs required for relations.
        id_order = int(order['id'])
        id_merchant = int(order['merchant_id_id'])
        
        t = self.apply_fee(amount)[0]
        f = self.apply_fee(amount)[1]
        c = datetime.now()
        o = Order.objects.get(pk=id_order)
        m = Merchant.objects.get(pk=id_merchant)

        # Create disembursement
        Disembursement.objects.create(
            merchant=m,
            order=o,
            fee_factor=f,
            total_amount=t,
            created_at=c,
        )

        return t

    # Dummy function that should mark the order as disembursed and to disemburse the money from the merchant.
    @classmethod
    def disemburse_from_merchant( self, merchant, amount, order):
        pass

    # Generates every single embursement sequentaly by reading the merchant orders 
    # returns a list of objects containg the total money to disemburse to each merchant.
    @classmethod
    def disembursements_generator(self):
        # Get orders grouped by merchants.
        merchants = Merchant.objects.all().values()
        list = []

        for merchant in merchants:
            id = merchant['id']
            # Get merchant orders marked as completed.
            orders = Order.objects.filter(
                merchant_id_id=id,
            ).exclude(
                completed_at=None
            ).values()
            total_amount = 0
            # Create disemburses
            for order in orders:
                # Skip current order if there is no amount.
                if order['amount'] == None:
                    continue
                amount = self.create_disemburse(order)
                total_amount += amount
                self.disemburse_from_merchant(merchant, amount, order)

            # Add total money and merchant info to the list
            dict = {
                "id": id,
                "merchant": merchant['name'],
                "total": round(total_amount, 2)
            }
            list.append(dict)
        return list
