from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from reservation.models import Reservation
from users.sms import send_appointment_reminder


class Command(BaseCommand):

    help = "ارسال پیامک یادآوری یک ساعت قبل از نوبت"

    def handle(self, *args, **options):

        now = timezone.localtime()

        target_start = now + timedelta(minutes=50)
        target_end = now + timedelta(minutes=70)

        reservations = Reservation.objects.filter(
            status="approved",
            reminder_sent=False,
            date=target_start.date(),
            time__gte=target_start.time(),
            time__lte=target_end.time(),
        )
        if not reservations.exists():
            self.stdout.write(
                "No appointment reminders to send."
            )
            return

        for reservation in reservations:

            phone = reservation.customer_phone

            if not phone:
                continue

            name = reservation.customer_name

            if reservation.user:
                name = reservation.user.full_name

            response = send_appointment_reminder(
                phone=phone,
                name=name,
                appointment_time=reservation.time.strftime("%H:%M"),
            )

            if response and response.status_code in [200, 201]:

                reservation.reminder_sent = True

                reservation.save(
                    update_fields=["reminder_sent"]
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Reminder sent to {phone}"
                    )
                )

            else:

                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to send reminder to {phone}"
                    )
                )