from __future__ import print_function

from datetime import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from abstract_is_candidate import AbstractIsCandidate
from abstract_is_examiner import AbstractIsExaminer
from basenode import BaseNode
from custom_db_fields import ShortNameField, LongNameField
from devilry.devilry_account.models import User, SubjectPermissionGroup
from model_utils import Etag
from node import Node


class SubjectQuerySet(models.QuerySet):
    def filter_user_is_admin(self, user):
        """
        Filter the queryset to only include :class:`.Subject` objects where the
        given ``user`` is in a :class:`.devilry.devilry_account.models.SubjectPermissionGroup`.

        Args:
            user: A User object.
        """
        if user.is_superuser:
            return self.all()
        else:
            subjectids_where_is_admin_queryset = SubjectPermissionGroup.objects \
                .filter(permissiongroup__users=user).values_list('subject_id', flat=True)
            return self.filter(id__in=subjectids_where_is_admin_queryset)


class Subject(models.Model, BaseNode, AbstractIsExaminer, AbstractIsCandidate, Etag):
    """

    .. attribute:: parentnode

        A django.db.models.ForeignKey_ that points to the parent node,
        which is always a `Node`_.

    .. attribute:: admins

        A django.db.models.ManyToManyField_ that holds all the admins of the
        `Node`_.

    .. attribute:: short_name

        A django.db.models.SlugField_ with max 20 characters. Only numbers,
        letters, '_' and '-'. Unlike all other children of
        :class:`BaseNode`, Subject.short_name is **unique**. This is mainly
        to avoid the overhead of having to recurse all the way to the top of
        the node hierarchy for every unique path.

    .. attribute:: periods

        A set of :class:`periods <devilry.apps.core.models.Period>` for this subject.

    .. attribute:: etag

       A DateTimeField containing the etag for this object.

    """
    objects = SubjectQuerySet.as_manager()

    class Meta:
        app_label = 'core'
        ordering = ['short_name']
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    short_name = ShortNameField(unique=True)
    long_name = LongNameField()
    parentnode = models.ForeignKey(Node, related_name='subjects',
                                   null=True, blank=True)
    admins = models.ManyToManyField(User, blank=True)
    etag = models.DateTimeField(auto_now_add=True)

    def get_path(self):
        """ Only returns :attr:`short_name` for subject since it is
        guaranteed to be unique. """
        return self.short_name
