import mock
from django import test
from django.conf import settings
from django_cradmin import cradmin_testhelpers
from model_mommy import mommy
from django.contrib import messages

from devilry.apps.core.models import AssignmentGroup
from devilry.devilry_admin.views.assignment.students import merge_groups
from devilry.apps.core import devilry_core_mommy_factories as core_mommy
from devilry.devilry_dbcache.customsql import AssignmentGroupDbCacheCustomSql


class TestMergeGroupsView(test.TestCase, cradmin_testhelpers.TestCaseMixin):
    """
    NOTE: Much of the functionality for this view is tested in
    test_groupview_base.test_groupviewmixin.TestGroupViewMixin
    and test_basemultiselectview.TestBaseMultiselectView.
    """
    viewclass = merge_groups.MergeGroupsView

    def setUp(self):
        AssignmentGroupDbCacheCustomSql().initialize()

    def __mockinstance_with_devilryrole(self, devilryrole):
        mockinstance = mock.MagicMock()
        mockinstance.get_devilryrole_for_requestuser.return_value = devilryrole
        return mockinstance

    def test_title(self):
        testassignment = mommy.make('core.Assignment', long_name='Test Assignment')
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'))
        self.assertIn(
            'Organize students in project groups',
            mockresponse.selector.one('title').alltext_normalized)

    def test_h1(self):
        testassignment = mommy.make('core.Assignment', long_name='Test Assignment')
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'))
        self.assertEqual(
            'Organize students in project groups',
            mockresponse.selector.one('h1').alltext_normalized)

    def test_groups_sanity(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        mommy.make('core.AssignmentGroup', parentnode=testassignment, _quantity=3)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'),
            requestuser=testuser)
        self.assertEqual(
            3,
            mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue'))

    def test_submit_button_text(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'),
            requestuser=testuser)
        self.assertEqual(
            'Create project group',
            mockresponse.selector.one('.django-cradmin-multiselect2-target-formfields .btn').alltext_normalized)

    def test_error_merge_less_than_2_groups(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group = mommy.make('core.AssignmentGroup', parentnode=testassignment, id=10)
        core_mommy.candidate(group=group)
        messagesmock = mock.MagicMock()
        self.mock_http302_postrequest(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'),
            requestuser=testuser,
            messagesmock=messagesmock,
            requestkwargs={
                'data': {
                    'selected_items': [10]
                }
            })
        messagesmock.add.assert_called_once_with(
            messages.WARNING,
            'Cannot merge less than 2 groups',
            ''
        )

    def test_success_merge_2_groups_message(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group1 = mommy.make('core.AssignmentGroup', parentnode=testassignment, id=10)
        group2 = mommy.make('core.AssignmentGroup', parentnode=testassignment, id=11)
        core_mommy.candidate(group=group1, shortname='April@example.com', fullname='April')
        core_mommy.candidate(group=group2, shortname='Dewey@example.com', fullname='Dewey')
        messagesmock = mock.MagicMock()
        self.mock_http302_postrequest(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'),
            requestuser=testuser,
            messagesmock=messagesmock,
            requestkwargs={
                'data': {
                    'selected_items': [10, 11]
                }
            })
        messagesmock.add.assert_called_once_with(
            messages.SUCCESS,
            'A group with April@example.com, Dewey@example.com has been created!',
            ''
        )

    def test_success_merge_2_groups_db(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        group1 = mommy.make('core.AssignmentGroup', parentnode=testassignment, id=10)
        group2 = mommy.make('core.AssignmentGroup', parentnode=testassignment, id=11)
        core_mommy.candidate(group=group1)
        core_mommy.candidate(group=group2)
        self.mock_http302_postrequest(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'),
            requestuser=testuser,
            requestkwargs={
                'data': {
                    'selected_items': [10, 11]
                }
            })
        self.assertTrue(AssignmentGroup.objects.filter(id=group1.id).exists())
        self.assertFalse(AssignmentGroup.objects.filter(id=group2.id).exists())
        self.assertEquals(AssignmentGroup.objects.get(id=group1.id).candidates.count(), 2)
        self.assertEquals(AssignmentGroup.objects.get(id=group1.id).feedbackset_set.count(), 2)
