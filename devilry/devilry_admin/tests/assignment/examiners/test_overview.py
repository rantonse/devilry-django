import mock
from django import test
from django.conf import settings
from django.http import Http404
from django_cradmin import cradmin_testhelpers
from model_mommy import mommy

from devilry.apps.core.models import Assignment
from devilry.devilry_admin.views.assignment.examiners import overview


class TestOverview(test.TestCase, cradmin_testhelpers.TestCaseMixin):
    viewclass = overview.Overview

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
            'Examiners on Test Assignment',
            mockresponse.selector.one('title').alltext_normalized)

    def test_h1(self):
        testassignment = mommy.make('core.Assignment', long_name='Test Assignment')
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'))
        self.assertEqual(
            'Examiners on Test Assignment',
            mockresponse.selector.one('h1').alltext_normalized)

    def test_buttonbar_sanity(self):
        testassignment = mommy.make('core.Assignment')
        mommy.make('core.RelatedExaminer', period=testassignment.period)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'))
        self.assertEqual(
            2,
            mockresponse.selector.count(
                '#devilry_admin_assignment_examiners_overview_buttonbar .btn'))

    def test_buttonbar_organize_examiners_link(self):
        testassignment = mommy.make('core.Assignment')
        mommy.make('core.RelatedExaminer', period=testassignment.period)
        mock_cradmin_instance = self.__mockinstance_with_devilryrole('departmentadmin')

        def mock_reverse_url(appname, viewname, **kwargs):
            return '/{}/{}'.format(appname, viewname)

        mock_cradmin_instance.reverse_url = mock_reverse_url
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=mock_cradmin_instance)
        self.assertEqual(
            # '/organize_examiners/INDEX',
            '#',
            mockresponse.selector
            .one('#devilry_admin_assignment_examiners_overview_button_organize_examiners')['href'])

    def test_buttonbar_organize_examiners_text(self):
        testassignment = mommy.make('core.Assignment')
        mommy.make('core.RelatedExaminer', period=testassignment.period)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'))
        self.assertEqual(
            'Organize examiners( Select students and assign one or more examiner )',
            mockresponse.selector
            .one('#devilry_admin_assignment_examiners_overview_button_organize_examiners')
            .alltext_normalized)

    def test_buttonbar_random_organize_examiners_link(self):
        testassignment = mommy.make('core.Assignment')
        mommy.make('core.RelatedExaminer', period=testassignment.period)
        mock_cradmin_instance = self.__mockinstance_with_devilryrole('departmentadmin')

        def mock_reverse_url(appname, viewname, **kwargs):
            return '/{}/{}'.format(appname, viewname)

        mock_cradmin_instance.reverse_url = mock_reverse_url
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=mock_cradmin_instance)
        self.assertEqual(
            # '/random_organize_examiners/INDEX',
            '#',
            mockresponse.selector
            .one('#devilry_admin_assignment_examiners_overview_button_random_organize_examiners')['href'])

    def test_buttonbar_random_organize_examiners_text(self):
        testassignment = mommy.make('core.Assignment')
        mommy.make('core.RelatedExaminer', period=testassignment.period)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'))
        self.assertEqual(
            'Organize examiners randomly( You choose a set of students and randomly assign '
            'some or all your examiners to those students. )',
            mockresponse.selector
            .one('#devilry_admin_assignment_examiners_overview_button_random_organize_examiners')
            .alltext_normalized)

    def test_examinerlist_no_relatedexaminers(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'),
            requestuser=testuser)
        self.assertTrue(mockresponse.selector.exists(
            '#devilry_admin_assignment_examiners_overview_no_relatedexaminers'))
        self.assertFalse(mockresponse.selector.exists('#django_cradmin_listbuilderview_listwrapper'))

    def test_has_relatedexaminers(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        mommy.make('core.RelatedExaminer', period=testassignment.period, _quantity=5)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testassignment,
            cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'),
            requestuser=testuser)
        self.assertTrue(mockresponse.selector.exists('#django_cradmin_listbuilderview_listwrapper'))
        self.assertEqual(5, mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue'))
        self.assertFalse(mockresponse.selector.exists(
            '#devilry_admin_assignment_examiners_overview_no_relatedexaminers'))

    #
    #
    # Anonymization tests
    #
    #

    def test_anonymizationmode_fully_anonymous_subjectadmin_404(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testgroup = mommy.make('core.AssignmentGroup',
                               parentnode=mommy.make_recipe(
                                   'devilry.apps.core.assignment_activeperiod_start',
                                   anonymizationmode=Assignment.ANONYMIZATIONMODE_FULLY_ANONYMOUS))
        with self.assertRaisesMessage(Http404, 'Only department admins have permission to edit examiners '
                                               'for fully anonymous assignments.'):
            self.mock_getrequest(
                cradmin_role=testgroup.assignment,
                cradmin_instance=self.__mockinstance_with_devilryrole('subjectadmin'),
                requestuser=testuser)

    def test_anonymizationmode_fully_anonymous_departmentadmin_no_404(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testgroup = mommy.make('core.AssignmentGroup',
                               parentnode=mommy.make_recipe(
                                   'devilry.apps.core.assignment_activeperiod_start',
                                   anonymizationmode=Assignment.ANONYMIZATIONMODE_FULLY_ANONYMOUS))
        self.mock_http200_getrequest_htmls(
                cradmin_role=testgroup.assignment,
                cradmin_instance=self.__mockinstance_with_devilryrole('departmentadmin'),
                requestuser=testuser)  # No Http404 exception raised!

    def test_anonymizationmode_semi_anonymous_subjectadmin_no_404(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testgroup = mommy.make('core.AssignmentGroup',
                               parentnode=mommy.make_recipe(
                                   'devilry.apps.core.assignment_activeperiod_start',
                                   anonymizationmode=Assignment.ANONYMIZATIONMODE_SEMI_ANONYMOUS))
        self.mock_http200_getrequest_htmls(
                cradmin_role=testgroup.assignment,
                cradmin_instance=self.__mockinstance_with_devilryrole('subjectadmin'),
                requestuser=testuser)  # No Http404 exception raised!
