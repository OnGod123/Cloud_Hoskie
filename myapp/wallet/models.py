from django.db import models
from myapp.models import Person  # Importing the Person model from your root app
import uuid
from datetime import timedelta, datetime

class UserWallet(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.person.name}'s Wallet"  # Adjust `name` to match your Person model fields


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('subscription', 'Subscription'),
    ]

    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    due_date = models.DateTimeField(default=lambda: datetime.now() + timedelta(days=60))

    def __str__(self):
        return f"{self.wallet.person.name} - {self.payment_type} - {self.amount}"  # Adjust `name` as needed

    def amount_value(self):
        return int(self.amount * 100)  # Convert to kobo for Paystack
