from django.db import models
import uuid
from myapp.models import Person
from django.utils.timezone import now
from datetime import timedelta
from myapp.wallet.models import Payment, UserWallet
import requests


class ConnectionLogic(models.Model):
    # Custom primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    from_user = models.ForeignKey(
        'Person', 
        related_name="sent_connections", 
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        'Person', 
        related_name="received_connections", 
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Connection from {self.from_user} to {self.to_user}"

def check_valid_payment_for_user(user):
    """
    Check if the user has a valid, successful payment within the last 60 days.

    Args:
    - user: A Person model instance (typically request.user in views).

    Returns:
    - True if the user has a valid, successful payment within 60 days.
    - False if the user does not have such a payment.
    """

    # Step 1: Get the User's Wallet through the Person model (using the user directly)
    wallet = UserWallet.objects.filter(person=user).first()  # Get the wallet related to the user

    if not wallet:
        # If the user doesn't have an associated wallet
        return False
    
    # Step 2: Check if there's a valid, successful payment for that wallet within the last 60 days
    valid_payment_exists = Payment.objects.filter(
        wallet=wallet,                           # Filter by the user's wallet
        is_successful=True,                      # Only consider successful payments
        due_date__gt=now() - timedelta(days=60)  # Ensure the payment is within the last 60 days
    ).exists()  # Use .exists() for efficiency, as we don't need the actual payment object

    return valid_payment_exists  # Returns True if a valid payment exists, otherwise False
