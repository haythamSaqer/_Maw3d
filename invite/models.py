from django.db import models
from datetime import datetime
import uuid

# Create your models here.
from accounts.models import UserAccount


def _get_invite_image_url(instance, filename):
    return f"invites/{instance.user.id}/images/{uuid.uuid4()}{filename}"


class Invite(models.Model):
    class TimeSlots(models.IntegerChoices):
        MINUTES_5 = 5, '5 minutes'
        MINUTES_10 = 10, '10 minutes'
        MINUTES_15 = 15, '15 minutes'
        MINUTES_20 = 20, '20 minutes'
        MINUTES_30 = 30, '30 minutes'
        HOUR_1 = 60, '1 hour'
        HOUR_2 = 120, '2 hours'

    class Type(models.TextChoices):
        one_on_one_invite = 'one_on_one_invite', 'one_on_one'
        group_invite = 'group_invite', 'group'

    class Location(models.TextChoices):
        type_empty = 'None'
        type_zoom = 'zoom'
        type_google = 'google'

    user = models.ForeignKey(
        UserAccount,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="user_invites",
    )
    inviteID = models.CharField(max_length=8, unique=True, primary_key=True, blank=True, editable=False)
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=50, choices=Location.choices),
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Name Invite #Url
    image = models.ImageField(
        "Invite Image",
        upload_to=_get_invite_image_url,
        default="/static/invites/images/placeholders/profile_image.jpg",
    )
    duration = models.DurationField()
    slotIncrement = models.IntegerField(default=TimeSlots.MINUTES_30, choices=TimeSlots.choices)
    created_time = models.DateTimeField(auto_now_add=datetime.now())
    starDate = models.CharField(max_length=150)
    endDate = models.CharField(max_length=150, null=True)
    type = models.CharField(max_length=50, choices=Type.choices, default=Type.one_on_one_invite),
    timezone = models.CharField(max_length=50)
    preventConflict = models.BooleanField()
    date_rang = models.DurationField()
    eventNameFormat = models.CharField(max_length=100, blank=True)
    TIMEZONE = ((0, 'Invitee Local Timezone'), (1, 'Locked Timezone'))
    displayedTimezone = models.IntegerField(default=TIMEZONE[0][0], choices=TIMEZONE)
    showIntro = models.BooleanField()
    showInYourProfilePage = models.BooleanField()
    minimumNotice = models.IntegerField()
    bufferBeforeEvent = models.IntegerField()  # Why ?
    bufferAfterEvent = models.IntegerField()  # Why ?
    limitMaxNumberEvents = models.BooleanField()
    maxNumberEvents = models.IntegerField()  # Why ?
    maxNumberEventsPer = models.CharField(max_length=100, blank=True)  # Why ?
    allowGuests = models.BooleanField()
    maxInvitees = models.IntegerField()
    link_invite = models.URLField(max_length=200, blank=True)

    def save(
            self, *args, **kwargs
    ):
        if not self.inviteID:
            self.inviteID = uuid.uuid4().hex[:8]
        if not self.slug:
            self.slug = self.inviteID
            self.link_invite = f'http://127.0.0.1:8000/api/invites/{self.slug}'
        else:
            self.link_invite = f'http://127.0.0.1:8000/api/invites/{self.slug}'

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Name : {self.name}, URL: {self.link_invite}'


class Availability(models.Model):
    invite = models.ForeignKey(Invite, on_delete=models.CASCADE, related_name='availability')
    duration = models.DurationField()
    rrule = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Availability"
        verbose_name_plural = "Invite Availability"
