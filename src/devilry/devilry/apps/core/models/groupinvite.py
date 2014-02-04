from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from devilry.utils.devilry_email import send_templated_message
from .assignment_group import AssignmentGroup



class GroupInviteQuerySet(models.query.QuerySet):
    def filter_accepted(self):
        return self.filter(accepted=True)

    def filter_rejected(self):
        return self.filter(accepted=False)

    def filter_no_response(self):
        return self.filter(accepted=None)


class GroupInviteManager(models.Manager):
    def get_queryset(self):
        return GroupInviteQuerySet(self.model, using=self._db)

    def filter(self, *args, **kwargs):
        return self.get_queryset().filter(*args, **kwargs)

    def all(self, *args, **kwargs):
        return self.get_queryset().filter(*args, **kwargs)

    def filter_accepted(self):
        return self.get_queryset().filter_accepted()

    def filter_rejected(self):
        return self.get_queryset().filter_rejected()

    def filter_no_response(self):
        return self.get_queryset().filter_no_response()


class GroupInvite(models.Model):
    """
    Represents a group invite sent by a student to invite another
    student to join their AssignmentGroup.

    To send an invite::

        invite = GroupInvite(
            group=myassignmentgroup,
            sent_by=somestudent, # Typically request.user
            sent_to=anotherstudent
        )
        invite.full_clean() # MUST be called to validate that the invite is allowed
        invite.save()
        invite.send_invite_notification()

    To accept/reject an invite (sets the appropriate attributes and sends a notification)::

        invite.respond(accepted=True)
    """
    group = models.ForeignKey(AssignmentGroup)
    sent_datetime = models.DateTimeField(default=datetime.now)
    sent_by = models.ForeignKey(User, related_name='groupinvite_sent_by_set')
    sent_to = models.ForeignKey(User, related_name='groupinvite_sent_to_set')

    accepted = models.NullBooleanField(default=None)
    responded_datetime = models.DateTimeField(
        default=None, blank=True, null=True)

    objects = GroupInviteManager()

    class Meta:
        app_label = 'core'

    def clean(self):
        if self.accepted and not self.responded_datetime:
            self.responded_datetime = datetime.now()
        if self.sent_by and not self.group.candidates.filter(student=self.sent_by).exists():
            raise ValidationError('The user sending an invite must be a Candiate on the group.')
        if self.sent_to and self.group.candidates.filter(student=self.sent_to).exists():
            raise ValidationError(_(u'The student is already a member of the group.'))

        assignment = self.group.assignment
        if assignment.students_can_create_groups:
            if assignment.students_can_not_create_groups_after and assignment.students_can_not_create_groups_after < datetime.now():
                raise ValidationError(_('Creating project groups without administrator approval is not allowed on this assignment anymore. Please contact you course administrator if you think this is wrong.'))
        else:
            raise ValidationError(_('This assignment does not allow students to form project groups on their own.'))

        period = assignment.period
        if not period.relatedstudent_set.filter(user=self.sent_to).exists():
            raise ValidationError(_('The invited student is not registered on this subject.'))

    def respond(self, accepted):
        self.accepted = accepted
        self.responded_datetime = datetime.now()
        self.full_clean()
        self.save()
        self._send_response_notification()

    def _send_response_notification(self):
        sent_to_displayname = self.sent_to.devilryuserprofile.get_displayname()
        if self.accepted:
            subject = _('{user} accepted your project group invite').format(user=sent_to_displayname)
            template_name = 'devilry_core/groupinvite_accepted.django.txt'
        else:
            subject = _('{user} rejected your project group invite').format(user=sent_to_displayname)
            template_name = 'devilry_core/groupinvite_rejected.django.txt'
        assignment = self.group.assignment
        send_templated_message(subject, template_name, {
            'sent_to_displayname': sent_to_displayname,
            'assignment': assignment.long_name,
            'subject': assignment.subject.long_name
        }, self.sent_by)

    def send_invite_notification(self, request):
        """
        Called to send the invite notification. Should be called
        right after creating the invite. Not called in save() to
        make message sending less coupled (to avoid any issues
        with testing and bulk creation of invites).

        :param request:
            A Django HttpRequest object. The only method used is
            the build_absolute_uri() method.

        :raise ValueError:
            If ``accepted==None``, or ``id==None``.
        """
        if self.accepted != None:
            raise ValueError('Can not send notification for an accepted GroupInvite.')
        elif self.id == None:
            raise ValueError('Can not send notification for an unsaved GroupInvite.')
        sent_by_displayname = self.sent_by.devilryuserprofile.get_displayname()
        assignment = self.group.assignment
        subject = _('Project group invite for {assignment}').format(assignment=assignment.get_path())
        template_name = 'devilry_core/groupinvite_invite.django.txt'
        url = request.build_absolute_uri(reverse('devilry_student_groupinvite_show', kwargs={'invite_id': self.id}))
        send_templated_message(subject, template_name, {
            'sent_by_displayname': sent_by_displayname,
            'assignment': assignment.long_name,
            'subject': assignment.subject.long_name,
            'url': url
        }, self.sent_to)
