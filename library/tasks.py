# loan/tasks.py
from django.utils import timezone

from celery import shared_task
from library.models import Loan
from library.services import send_telegram_message


@shared_task(bind=True)
def send_loan_reminder(loan_id):
    loan = Loan.objects.get(id=loan_id)
    if loan.is_active:
        return

    print('TASK STARTED', loan_id)
    message = f'⏰ Напоминание!\n\n До возврата книги {loan.book.title} осталось 2 дня'

    send_telegram_message(
        chat_id=loan.user.telegram_chat_id,
        text=message
    )


@shared_task
def update_overdue_loans():
    now = timezone.now()

    Loan.objects.filter(
        return_at__lt=now,
        returned_at__isnull=True,
        is_overdue=False
    ).update(is_overdue=True)


@shared_task
def send_overdue_reminders():
    now = timezone.now()

    overdue_loans = Loan.objects.filter(
        is_overdue=True,
        returned_at__isnull=True
    )

    for loan in overdue_loans:
        message = f'⏰ Напоминание!\n\n Книга {loan.book.title} просрочена на {(now - loan.return_at).days} дней!\n '

        send_telegram_message(
            chat_id=loan.user.telegram_chat_id,
            text=message
        )

