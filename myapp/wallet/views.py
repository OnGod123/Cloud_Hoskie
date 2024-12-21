from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import Payment
import requests
import logging

# Set up logging for errors
logger = logging.getLogger(__name__)

def initiate_payment(request, payment_type):
    try:
        # Validate payment type
        if payment_type not in ['deposit', 'subscription']:
            return JsonResponse({'error': 'Invalid payment type'}, status=400)

        if request.method == "POST":
            amount = request.POST.get('amount')
            email = request.POST.get('email')

            # Validate input data
            if not amount or not email:
                return JsonResponse({'error': 'Amount and email are required.'}, status=400)
            if not amount.isdigit() or int(amount) <= 0:
                return JsonResponse({'error': 'Amount must be a positive number.'}, status=400)

            # Create a Payment instance
            payment = Payment.objects.create(
                amount=float(amount),
                email=email,
                user=request.user,
                payment_type=payment_type,
            )

            # Initialize Paystack transaction
            paystack = Paystack()
            status, response = paystack.initialize_payment(payment)
            if status:
                return JsonResponse({'payment': response})
            else:
                # Log errors for debugging
                logger.error(f"Paystack initialization failed: {response}")
                return JsonResponse({'error': 'Failed to initialize payment. Try again later.'}, status=500)

        return render(request, 'payment.html', {'payment_type': payment_type})

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"An unexpected error occurred: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred. Please try again later.'}, status=500)


class Paystack:
    PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co/"

    def initialize_payment(self, payment):
        try:
            url = f"{self.base_url}transaction/initialize"
            headers = {
                "Authorization": f"Bearer {self.PAYSTACK_SK}",
                "Content-Type": "application/json",
            }
            data = {
                "email": payment.email,
                "amount": payment.amount_value(),
                "reference": str(payment.ref),
            }
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return True, response_data['data']
            else:
                # Log API failure response
                logger.error(f"Paystack API error: {response.json()}")
                return False, response.json()

        except requests.exceptions.RequestException as e:
            # Handle request errors
            logger.error(f"Paystack request failed: {str(e)}")
            return False, {'error': 'Paystack API request failed. Check your internet connection.'}

        except Exception as e:
            # Catch all unexpected errors
            logger.error(f"Unexpected error in Paystack initialization: {str(e)}")
            return False, {'error': 'An unexpected error occurred while initializing payment.'}
