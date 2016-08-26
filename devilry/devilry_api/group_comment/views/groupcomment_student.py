from rest_framework.generics import mixins

from devilry.apps.core.models import AssignmentGroup
from devilry.devilry_api.group_comment.serializers.serializer_student import GroupCommentSerializerStudent
from devilry.devilry_api.group_comment.views.groupcomment_base import BaseGroupCommentView
from devilry.devilry_api.models import APIKey
from devilry.devilry_api.permission.student_permission import StudentPermissionAPIKey
from devilry.devilry_group.models import GroupComment


class GroupCommentViewStudent(mixins.CreateModelMixin,
                              BaseGroupCommentView):
    permission_classes = (StudentPermissionAPIKey, )
    api_key_permissions = (APIKey.STUDENT_PERMISSION_READ, APIKey.STUDENT_PERMISSION_WRITE)
    serializer_class = GroupCommentSerializerStudent

    def get_role_query_set(self):
        """
        Returns role queryset for student role

        Returns:
            :class:`~devilry_group.GroupComment` queryset
        """
        assignment_group_queryset = AssignmentGroup.objects.filter_student_has_access(user=self.request.user)
        return GroupComment.objects.filter(feedback_set__group=assignment_group_queryset,
                                           comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
                                           visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)

    def get(self, request, feedback_set, *args, **kwargs):
        return super(GroupCommentViewStudent, self).get(request, feedback_set, *args, **kwargs)

    get.__doc__ = BaseGroupCommentView.get.__doc__

    def post(self, request, feedback_set, *args, **kwargs):
        """
        post a comment to a feedbackset

        ---
        parameters:
            - name: feedback_set
              required: true
              paramType: path
              type: Int
              description: feedbackset id
            - name: text
              required: true
              paramType: form
              type: String
              description: comment text
        """
        request.POST._mutable = True
        request.data['feedback_set'] = feedback_set
        request.data['user_role'] = GroupComment.USER_ROLE_STUDENT
        return super(GroupCommentViewStudent, self).create(request, *args, **kwargs)
