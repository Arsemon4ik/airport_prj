import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
import requests
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


class MonoBankService:
    def __init__(self, token=settings.MONOBANK_TOKEN):
        self.invoice_url = "https://api.monobank.ua/api/merchant/invoice/create"
        self.headers = {"X-Token": token}

    def create_invoice(self, transaction_id, description, order_total):
        """
        Creates a Monobank payment invoice.
        """
        payload = {
            "amount": int(order_total * 100),
            "merchantPaymInfo": {
                "reference": str(transaction_id),
                "destination": description
            },
            "redirectUrl": settings.PUBLIC_HOST + reverse('booking_list'),
            "webHookUrl": settings.PUBLIC_HOST + reverse('monopay_callback'),
        }

        try:
            response = requests.post(self.invoice_url, headers=self.headers, json=payload)
            response.raise_for_status()
            invoice_data = response.json()
            return invoice_data.get('pageUrl', '')
        except requests.exceptions.RequestException as e:
            logger.error(f'Error in create_invoice: {e}')


def send_order_confirmation_email(booking):
    html_content = render_to_string('booking_management/email.html', {'booking': booking})
    plain_message = strip_tags(html_content)

    email_message = EmailMultiAlternatives(
        subject=f'Дякуємо, що обрали нас! Ваш квиток №{booking.booking_code}',
        body=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[booking.passenger.email]
    )

    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()
