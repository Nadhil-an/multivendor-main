from django.db import models
from accounts.models import User, UserProfile
from accounts.utilis import send_approve_mail
from django.template.defaultfilters import slugify
from datetime import time, datetime, date


# ---------------------------------------------------
# Vendor Model
# ---------------------------------------------------
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userProfile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_licence = models.ImageField(upload_to='vendor/licence')
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def is_open(self):
        """Check if the vendor is open based on today's hours."""
        today = date.today().isoweekday()
        now = datetime.now().time()
        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)

        for i in current_opening_hours:

            # Skip invalid or blank times
            if not i.from_hour or not i.to_hour:
                continue

            # Convert from_hour safely
            if isinstance(i.from_hour, str):
                try:
                    start_time = datetime.strptime(i.from_hour.strip(), "%I:%M:%p").time()
                except ValueError:
                    try:
                        start_time = datetime.strptime(i.from_hour.strip(), "%H:%M:%S").time()
                    except ValueError:
                        continue  # invalid time → skip entry
            else:
                start_time = i.from_hour

            # Convert to_hour safely
            if isinstance(i.to_hour, str):
                try:
                    end_time = datetime.strptime(i.to_hour.strip(), "%I:%M:%p").time()
                except ValueError:
                    try:
                        end_time = datetime.strptime(i.to_hour.strip(), "%H:%M:%S").time()
                    except ValueError:
                        continue
            else:
                end_time = i.to_hour

            # Check if vendor is open now
            if start_time <= now <= end_time and not i.is_closed:
                return True

        # If no matched open slot
        return False

    def save(self, *args, **kwargs):
        # Auto-generate slug if it doesn't exist
        if not self.vendor_slug and self.user_id:
            self.vendor_slug = slugify(self.vendor_name) + '-' + str(self.user.id)

        # Send approval email when the status is changed
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/vendor_email.html'
                context = {'user': self.user, 'is_approved': self.is_approved}
                mail_subject = (
                    'Congratulations, Your Restaurant Menu was Approved'
                    if self.is_approved else
                    'Restaurant Menu was Rejected'
                )
                send_approve_mail(mail_template, context, mail_subject)

        super().save(*args, **kwargs)


# ---------------------------------------------------
# OpeningHour Model
# ---------------------------------------------------
DAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]

# Generates choices like 12:00 AM, 12:30 AM, ... 11:30 PM
HOURS_OF_24 = [
    (time(h, m).strftime('%I:%M:%p'), time(h, m).strftime('%I:%M:%p'))
    for h in range(0, 24)
    for m in (0, 30)
]


class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOURS_OF_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOURS_OF_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', 'from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()

    @classmethod
    def get_day_name_from_value(cls, day_value):
        return dict(cls._meta.get_field('day').choices).get(day_value, 'Unknown Day')
