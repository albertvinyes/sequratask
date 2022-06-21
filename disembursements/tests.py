from gc import disable
from disembursements.models import DisembursementController, Disembursement
from merchants.models import Merchant
from orders.models import Order
from shoppers.models import Shopper
from django.test import TestCase
from django.utils import timezone
import datetime

class DisembursementsTests(TestCase):

    def setUp(self):
        # IDs
        self.merchant_id = -1
        self.shopper_id = -1
        self.order_id = -1
        self.disembursement_id = -1
        # Relational objects
        self.merchant = None
        self.shopper = None
        self.order = None
        pass

    def test_create_merchant(self):
        message = "Could not create merchant."
        self.merchant_id = int(Merchant.objects.create(
            id="90000",
            name="Aaaah Stranger",
            email="what@areyoubuying.com",
            cif="HEHETHANKYOU"
        ).id)
        self.order = Merchant.objects.get(pk=self.merchant_id)
        self.assertGreater(self.merchant_id, -1, message)

    def test_create_shopper(self):
        message = "Could not create shopper."
        self.shopper_id = int(Shopper.objects.create(
            id="90000",
            name="Leon S. Kennedy",
            email="mustprotect@claire.com",
            nif="0000000007"
        ).id)
        self.shopper = Shopper.objects.get(pk=self.shopper_id)
        self.assertGreater(self.shopper_id, -1, message)

    def test_create_order(self):
        message = "Could not create order."
        self.order_id = int(Order.objects.create(
            id="90000",
            merchant_id=self.merchant,
            shopper_id=self.shopper,
            amount="300",
            created_at="01/01/2018 15:12:00",
            completed_at=None,
            disembursed=False
        ).id)
        self.assertGreater(self.order_id, 0, message)


    def test_create_disembursement(self):
        message = "Could not create disembursement."
        self.disembursement_id = int(Disembursement.objects.create(
            merchant_id=self.merchant,
            order_id=self.shopper,
            fee_factor=1.0100,
            total_amount=10.01,
            created_at="01/01/2018 15:12:01",
        ).id)
        self.assertGreater(self.disembursement_id, 0, message)

    def tearDown(self):
        Merchant.objects.filter(id=self.merchant_id).delete()
        Order.objects.filter(id=self.order_id).delete()
        Shopper.objects.filter(id=self.shopper_id).delete()
        Disembursement.objects.filter(id=self.disembursement_id).delete()