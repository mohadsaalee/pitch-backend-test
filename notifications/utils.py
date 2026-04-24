from .models import Notification


def create_notification(recipient, sender, notif_type, message):
    if recipient == sender:
        return
    Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notif_type=notif_type,
        message=message,
    )
