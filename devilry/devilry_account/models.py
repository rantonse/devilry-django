from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Manager for :class:`User`.
    """


class User(AbstractBaseUser):
    """
    User model for Devilry.
    """
    objects = UserManager()

    #: Is this user a superuser?
    is_superuser = models.BooleanField(
        verbose_name=_('superuser status'),
        default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))

    #: Short name for the user.
    #: This will be set to the primary email address or to the primary username
    #: depending on the auth backend.
    shortname = models.CharField(
        max_length=255,
        blank=False, null=False,
        editable=False,
        help_text=_('The short name for the user. This is set automatically to the '
                    'email or username based ')
    )

    #: Full name of the user. Optional.
    fullname = models.TextField(
        verbose_name=_('Full name'),
        blank=True, default="", null=False)

    #: The last name of the user. Optional.
    #: Used to sort by last name.
    lastname = models.TextField(
        verbose_name=_('Last name'),
        blank=True, default="", null=False)

    #: The datetime the user was created.
    datetime_joined = models.DateTimeField(
        verbose_name=_('date joined'),
        default=timezone.now)

    #: Datetime when this account was suspended.
    suspended_datetime = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('Suspension time'),
        help_text=_('Time when the account was suspended'))

    #: Reason why the account is suspended.
    suspended_reason = models.TextField(
        blank=True, default='',
        verbose_name=_('Reason for suspension'))

    #: The language code for the preferred language for the user.
    languagecode = models.CharField(
        max_length=10, blank=True, null=False,
        default='',
        verbose_name=_('Preferred language')
    )

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['short_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_active(self):
        return self.suspended_datetime is None

    def get_full_name(self):
        """
        Get the :obj:`~.User.fullname`, falling back to :obj:`~.User.shortname`
        if fullname is not set.
        """
        return self.fullname or self.shortname

    def get_short_name(self):
        """
        Get the short name for the user.
        """
        return self.shortname

    def __str__(self):
        return self.shortname

    def clean(self):
        if self.suspended_datetime is None and self.suspended_reason != '':
            raise ValidationError(_('Can not provide a reason for suspension when suspension time is blank.'))


class AbstractUserIdentity(models.Model):
    class Meta:
        abstract = True

    #: Foreign key to the user owning this email address.
    user = models.ForeignKey(User)

    #: The datetime when this was created.
    created_datetime = models.DateTimeField(
        default=timezone.now(),
        editable=False,
        null=False, blank=False)

    #: The datetime when this was last updated.
    last_updated_datetime = models.DateTimeField(
        default=timezone.now(),
        editable=False,
        null=False, blank=False)

    def clean(self):
        self.last_updated_datetime = timezone.now()


class UserEmail(AbstractUserIdentity):
    """
    Stores a single email address for a :class:`.User`.
    """
    class Meta:
        verbose_name = _('Email address')
        verbose_name_plural = _('Email addresses')

    #: The email address of the user.
    #: Must be unique.
    email = models.EmailField(
        verbose_name=_('Email'),
        unique=True,
        max_length=255)

    #: Is this a notification email for the user?
    #: A user can have multiple notification emails.
    use_for_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Send notifications to this email address?'))


class UserName(AbstractUserIdentity):

    """
    Stores a single username for a :class:`.User`.

    The username is used for login, and the primary username
    is synced into :obj:`.User.shortname`.
    """
    class Meta:
        verbose_name = _('Username')
        verbose_name_plural = _('Usernames')
        unique_together = [
            ('user', 'is_primary')
        ]

    #: The username of the user.
    #: Must be unique.
    username = models.CharField(
        verbose_name=_('Username'),
        unique=True,
        max_length=255)

    #: Is this the primary username for the user?
    #: Valid values are: ``None`` and ``True``, and only
    #: one UserName per user can have ``is_primary=True``.
    is_primary = models.NullBooleanField(
        verbose_name=_('Is this your primary username?'),
        choices=[
            (None, _('No')),
            (True, _('Yes'))
        ],
        help_text=_('Your primary username is shown alongside your full '
                    'name to identify you to teachers, examiners and '
                    'other students.')
    )