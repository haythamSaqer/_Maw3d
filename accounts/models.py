import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from social_django.models import UserSocialAuth
from datetime import datetime, date


def _get_profile_image_url(instance, filename):
    return f"accounts/{instance.user.id}/images/{uuid.uuid4()}{filename}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def _str_(self):
        return self.email

    class Meta:
        verbose_name_plural = "User Accounts"

class Profile(models.Model):
    user = models.OneToOneField(
        UserAccount,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="userprofile",
    )
    image = models.ImageField(
        "Profile Image",
        upload_to=_get_profile_image_url,
        default="/static/accounts/images/placeholders/profile_image.jpg",
    )
    imageProvider = models.URLField(max_length=250, blank=True, null=True)
    accessTokenProvider = models.TextField(blank=True, null=True)
    refreshTokenProvider = models.TextField(blank=True, null=True)
    scopes = models.TextField(blank=True, null=True)
    has_calender = models.BooleanField(default=False)
    numberOfInvitationsLicence = models.IntegerField(default=1)
    invitations_counter = models.CharField(null=True, blank=True, max_length=100)
    subscribed = models.BooleanField(default=False)
    SUBSCRIPTION_OPTIONS = (('free', 'Free'), ('starter', '6 Month Licence'), ('advance', '12 Month Licence'))
    subscriptionType = models.CharField(max_length=100, choices=SUBSCRIPTION_OPTIONS,
                                        default=SUBSCRIPTION_OPTIONS[0][0])
    subscriptionID = models.CharField(null=True, blank=True, max_length=100)
    subscriptionReference = models.CharField(null=True, blank=True, max_length=500)
    paid_until = models.DateField(
        null=True,
        blank=True
    )

    def set_paid_until(self, date_or_timestamp):
        if isinstance(date_or_timestamp, int):
            paid_until = date.fromtimestamp(date_or_timestamp)
        elif isinstance(date_or_timestamp, str):
            paid_until = date.fromtimestamp(int(date_or_timestamp))
        else:
            paid_until = date_or_timestamp
        self.paid_until = paid_until
        self.save()

    # if user.has_paid  => PRO Account : Upgrade to PRO
    def has_paid(self, current_date=datetime.today()):
        if self.paid_until is None:
            return False
        return current_date < self.paid_until

    # scope = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email


class Availability(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='defaultWeekAvailability')
    duration = models.DurationField()
    rrule = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Availability"
        verbose_name_plural = "User Availability"


def extract_use_calender(urls: str):
    from urllib.parse import urlparse
    import validators
    get_urls = urls.split(' ')
    has_permission_calendar = False
    for url in get_urls:
        if validators.url(url):
            parsed_url = urlparse(url)
            captured_value = True if '/auth/calendar' in parsed_url.path else False
            if captured_value:
                has_permission_calendar = True

    return has_permission_calendar


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        profile = user.userprofile if hasattr(user, 'userprofile') else None
        if profile is None:
            profile = Profile.objects.create(user_id=user.id)
        profile.imageProvider = response.get('picture')
        profile.accessTokenProvider = response.get('access_token')
        profile.refreshTokenProvider = response.get('refresh_token')
        profile.scopes = response.get('scope')
        has_calendar = extract_use_calender(response.get('scope'))
        profile.has_calender = has_calendar
        profile.save()
