import logging
from django.conf import settings
from .models import WebhookSubscription

logger = logging.getLogger(__name__)

def send_webhook_notification(event, payload):
    try:
        import requests
    except ImportError:
        logger.error("Requests library is not installed. Unable to send webhook notifications.")
        return

    subscriptions = WebhookSubscription.objects.filter(event=event, is_active=True)
    
    for subscription in subscriptions:
        try:
            response = requests.post(
                subscription.target_url,
                json={
                    'event': event,
                    'payload': payload
                },
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            response.raise_for_status()
            logger.info(f"Webhook sent successfully to {subscription.target_url} for event {event}")
        except requests.RequestException as e:
            logger.error(f"Failed to send webhook to {subscription.target_url} for event {event}: {str(e)}")
            # Here you might want to implement some error handling,
            # such as marking the subscription as inactive after multiple failures
        except Exception as e:
            logger.error(f"Unexpected error when sending webhook to {subscription.target_url} for event {event}: {str(e)}")

def mock_send_webhook_notification(event, payload):
    logger.info(f"Mock webhook notification: Event: {event}, Payload: {payload}")

# Choose the appropriate function based on settings
if getattr(settings, 'USE_MOCK_WEBHOOKS', False):
    send_webhook = mock_send_webhook_notification
else:
    send_webhook = send_webhook_notification