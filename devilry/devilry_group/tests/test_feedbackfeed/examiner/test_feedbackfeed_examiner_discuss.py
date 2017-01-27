# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from model_mommy import mommy

from devilry.devilry_comment import models as comment_models
from devilry.devilry_dbcache.customsql import AssignmentGroupDbCacheCustomSql
from devilry.devilry_group import devilry_group_mommy_factories as group_mommy
from devilry.devilry_group import models as group_models
from devilry.apps.core import models as core_models
from devilry.devilry_group.tests.test_feedbackfeed.mixins import test_feedbackfeed_examiner
from devilry.devilry_group.views.examiner import feedbackfeed_examiner


class TestFeedbackfeedExaminerDiscussMixin(test_feedbackfeed_examiner.TestFeedbackfeedExaminerMixin):

    def test_get_examiner_first_attempt_feedback_tab_does_not_exist_if_last_feedbackset_is_published(self):
        testgroup = mommy.make('core.AssignmentGroup')
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertFalse(mockresponse.selector.exists('.devilry-group-feedbackfeed-feedback-button'))

    def test_get_examiner_first_attempt_feedback_tab_exist_if_last_feedbackset_is_unpublished(self):
        testgroup = mommy.make('core.AssignmentGroup')
        group_mommy.feedbackset_first_attempt_unpublished(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertTrue(mockresponse.selector.exists('.devilry-group-feedbackfeed-feedback-button'))

    def test_get_examiner_new_attempt_feedback_tab_does_not_exist_if_last_feedbackset_is_published(self):
        testgroup = mommy.make('core.AssignmentGroup')
        group_mommy.feedbackset_new_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertFalse(mockresponse.selector.exists('.devilry-group-feedbackfeed-feedback-button'))

    def test_get_examiner_new_attempt_feedback_tab_exist_if_last_feedbackset_is_unpublished(self):
        testgroup = mommy.make('core.AssignmentGroup')
        group_mommy.feedbackset_new_attempt_unpublished(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertTrue(mockresponse.selector.exists('.devilry-group-feedbackfeed-feedback-button'))

    def test_get_examiner_first_attempt_unpublished_alert_choice_box_does_not_exist(self):
        # Tests that box providing the possibility of giving a new attempt or re-edit does NOT show when last
        # feedbackset has been NOT been published.
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertFalse(
            mockresponse.selector.exists('.devilry-group-feedbackfeed-examiner-after-publish-choice-alert'))

    def test_get_examiner_first_attempt_published_choice_alert_box_exists(self):
        # Tests that box providing the possibility of giving a new attempt shows when last feedbackset has been
        # published
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertTrue(
            mockresponse.selector.exists('.devilry-group-feedbackfeed-examiner-after-publish-choice-alert'))

    def test_get_examiner_first_attempt_published_choice_alert_info_text(self):
        # Test the info-text in the alert box that show when the last feedbackset is published.
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        choice_alert_info_text = mockresponse.selector.one(
            '.devilry-group-feedbackfeed-examiner-after-publish-choice-alert-info-text'
        ).alltext_normalized
        self.assertEquals(
            'The first attempt has been graded. You can leave this grade '
            'as their final grade for this assignment, or:',
            choice_alert_info_text
        )

    def test_get_examiner_first_attempt_published_choice_alert_new_attempt_button(self):
        # Test that new attempt button exists in the choice alert when last feedbackset is published.
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertTrue(
            mockresponse.selector.exists(
                '.devilry-group-feedbackfeed-examiner-after-publish-choice-alert-new-attempt-button')
        )
        button_text = mockresponse.selector \
            .one(
            '.devilry-group-feedbackfeed-examiner-after-publish-choice-alert-new-attempt-button').alltext_normalized
        self.assertEquals('Give new attempt', button_text)

    def test_get_examiner_first_attempt_published_choice_alert_re_edit_button_text(self):
        # Test that new attempt button exists in the choice alert when last feedbackset is published.
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertTrue(
            mockresponse.selector.exists(
                '.devilry-group-feedbackfeed-examiner-after-publish-choice-alert-reedit-button')
        )
        button_text = mockresponse.selector \
            .one('.devilry-group-feedbackfeed-examiner-after-publish-choice-alert-reedit-button').alltext_normalized
        self.assertEquals('Edit the grade', button_text)

    def test_get_examiner_new_attempt_unpublished_choice_alert_does_not_exist(self):
        # Test that choice alert for giving a new attempt or re editing the last does NOT show
        # when first feedbackset is published, but the new try is unpublished.
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        testfeedbackset_new_attempt = group_mommy.feedbackset_new_attempt_unpublished(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertNotEquals(testgroup.cached_data.last_published_feedbackset, testfeedbackset_new_attempt)
        self.assertEquals(testgroup.cached_data.last_feedbackset, testfeedbackset_new_attempt)
        self.assertFalse(
            mockresponse.selector.exists('.devilry-group-feedbackfeed-examiner-after-publish-choice-alert')
        )

    def test_get_examiner_new_attempt_published_choice_alert_exists(self):
        # Tests that choice alert for giving new attempt or re editing the last shows
        # when first feedbackset and new attempt is published.
        testassignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
        testgroup = mommy.make('core.AssignmentGroup', parentnode=testassignment)
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        testfeedbackset_new_attempt = group_mommy.feedbackset_new_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertEquals(testgroup.cached_data.last_published_feedbackset, testfeedbackset_new_attempt)
        self.assertEquals(testgroup.cached_data.last_feedbackset, testfeedbackset_new_attempt)
        self.assertTrue(
            mockresponse.selector.exists('.devilry-group-feedbackfeed-examiner-after-publish-choice-alert')
        )

    def test_post_comment_always_to_last_feedbackset(self):
        assignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start',
                                       grading_system_plugin_id=core_models.Assignment
                                       .GRADING_SYSTEM_PLUGIN_ID_PASSEDFAILED)
        group = mommy.make('core.AssignmentGroup', parentnode=assignment)
        examiner = mommy.make('core.Examiner',
                              assignmentgroup=group,
                              relatedexaminer=mommy.make('core.RelatedExaminer'))
        feedbackset_first = group_mommy.feedbackset_first_attempt_published(group=group)
        feedbackset_last = group_mommy.feedbackset_new_attempt_unpublished(group=group)
        self.mock_http302_postrequest(
            cradmin_role=examiner.assignmentgroup,
            requestuser=examiner.relatedexaminer.user,
            viewkwargs={'pk': group.id},
            requestkwargs={
                'data': {
                    'text': 'This is a feedback',
                    'examiner_add_public_comment': 'unused value',
                }
            })
        comments = group_models.GroupComment.objects.all()
        self.assertEquals(len(comments), 1)
        self.assertNotEquals(feedbackset_first, comments[0].feedback_set)
        self.assertEquals(feedbackset_last, comments[0].feedback_set)
        self.assertEquals(2, group_models.FeedbackSet.objects.count())


class TestFeedbackfeedExaminerPublicDiscuss(TestCase, TestFeedbackfeedExaminerDiscussMixin):
    viewclass = feedbackfeed_examiner.ExaminerPublicDiscussView

    def setUp(self):
        AssignmentGroupDbCacheCustomSql().initialize()

    def test_get_examiner_add_comment_button(self):
        testgroup = mommy.make('core.AssignmentGroup')
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertTrue(mockresponse.selector.exists('#submit-id-examiner_add_public_comment'))
        self.assertEquals(
            'Add comment',
            mockresponse.selector.one('#submit-id-examiner_add_public_comment').alltext_normalized
        )

    def test_get_examiner_form_heading(self):
        testgroup = mommy.make('core.AssignmentGroup')
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertTrue(mockresponse.selector.exists('.devilry-group-feedbackfeed-form-heading'))
        self.assertEquals(
            'Here you can discuss with students and examiners on the group, as well as admins. '
            'You can also upload files. The uploaded files will be visible to everyone with access to this group.',
            mockresponse.selector.one('.devilry-group-feedbackfeed-form-heading').alltext_normalized
        )

    def test_post_first_attempt_unpublished_comment_with_text(self):
        testgroup = mommy.make('core.AssignmentGroup')
        group_mommy.feedbackset_first_attempt_unpublished(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        self.mock_http302_postrequest(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user,
            viewkwargs={'pk': testgroup.id},
            requestkwargs={
                'data': {
                    'text': 'This is a comment',
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        posted_comment = group_models.GroupComment.objects.all()[0]
        self.assertEquals(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE,
                          posted_comment.visibility)
        self.assertEquals('This is a comment', posted_comment.text)

    def test_post_first_attempt_published_comment_with_text(self):
        testgroup = mommy.make('core.AssignmentGroup')
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        self.mock_http302_postrequest(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user,
            viewkwargs={'pk': testgroup.id},
            requestkwargs={
                'data': {
                    'text': 'This is a comment',
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        posted_comment = group_models.GroupComment.objects.all()[0]
        self.assertEquals(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE,
                          posted_comment.visibility)
        self.assertEquals('This is a comment', posted_comment.text)

    def test_post_new_attempt_unpublished_comment_with_text(self):
        testgroup = mommy.make('core.AssignmentGroup')
        testfeedbackset = group_mommy.feedbackset_new_attempt_unpublished(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        self.mock_http302_postrequest(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user,
            viewkwargs={'pk': testgroup.id},
            requestkwargs={
                'data': {
                    'text': 'This is a comment',
                }
            })
        self.assertEquals(2, group_models.FeedbackSet.objects.count())
        last_feedbackset = group_models.FeedbackSet.objects.all()[1]
        self.assertEquals(last_feedbackset, testfeedbackset)
        self.assertEquals(1, group_models.GroupComment.objects.count())
        posted_comment = group_models.GroupComment.objects.all()[0]
        self.assertEquals(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE,
                          posted_comment.visibility)
        self.assertEquals('This is a comment', posted_comment.text)

    def test_post_new_attempt_published_comment_with_text(self):
        testgroup = mommy.make('core.AssignmentGroup')
        testfeedbackset = group_mommy.feedbackset_new_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        self.mock_http302_postrequest(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user,
            viewkwargs={'pk': testgroup.id},
            requestkwargs={
                'data': {
                    'text': 'This is a comment',
                }
            })
        self.assertEquals(2, group_models.FeedbackSet.objects.count())
        last_feedbackset = group_models.FeedbackSet.objects.all()[1]
        self.assertEquals(last_feedbackset, testfeedbackset)
        self.assertEquals(1, group_models.GroupComment.objects.count())
        posted_comment = group_models.GroupComment.objects.all()[0]
        self.assertEquals(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE,
                          posted_comment.visibility)
        self.assertEquals('This is a comment', posted_comment.text)


class TestFeedbackfeedExaminerWithAdminDiscuss(TestCase, TestFeedbackfeedExaminerDiscussMixin):
    viewclass = feedbackfeed_examiner.ExaminerWithAdminsDiscussView

    def setUp(self):
        AssignmentGroupDbCacheCustomSql().initialize()

    def test_get_examiner_add_comment_button(self):
        testgroup = mommy.make('core.AssignmentGroup')
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertTrue(mockresponse.selector.exists('#submit-id-examiner_add_comment_for_examiners_and_admins'))
        self.assertEquals(
            'Add comment',
            mockresponse.selector.one('#submit-id-examiner_add_comment_for_examiners_and_admins').alltext_normalized
        )

    def test_get_examiner_form_heading(self):
        testgroup = mommy.make('core.AssignmentGroup')
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        mockresponse = self.mock_http200_getrequest_htmls(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user
        )
        self.assertTrue(mockresponse.selector.exists('.devilry-group-feedbackfeed-form-heading'))
        self.assertEquals(
            'Here you can discuss with other examiners on the group and admins - no students. '
            'You can also upload files. The uploaded files will only be visible to '
            'examiners and admins with access to this group.',
            mockresponse.selector.one('.devilry-group-feedbackfeed-form-heading').alltext_normalized
        )

    def test_post_first_attempt_unpublished_comment_with_text(self):
        testgroup = mommy.make('core.AssignmentGroup')
        group_mommy.feedbackset_first_attempt_unpublished(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        self.mock_http302_postrequest(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user,
            viewkwargs={'pk': testgroup.id},
            requestkwargs={
                'data': {
                    'text': 'This is a comment',
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        posted_comment = group_models.GroupComment.objects.all()[0]
        self.assertEquals(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS,
                          posted_comment.visibility)
        self.assertEquals('This is a comment', posted_comment.text)

    def test_post_first_attempt_published_comment_with_text(self):
        testgroup = mommy.make('core.AssignmentGroup')
        group_mommy.feedbackset_first_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        self.mock_http302_postrequest(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user,
            viewkwargs={'pk': testgroup.id},
            requestkwargs={
                'data': {
                    'text': 'This is a comment',
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        posted_comment = group_models.GroupComment.objects.all()[0]
        self.assertEquals(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS,
                          posted_comment.visibility)
        self.assertEquals('This is a comment', posted_comment.text)

    def test_post_new_attempt_unpublished_comment_with_text(self):
        testgroup = mommy.make('core.AssignmentGroup')
        testfeedbackset = group_mommy.feedbackset_new_attempt_unpublished(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        self.mock_http302_postrequest(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user,
            viewkwargs={'pk': testgroup.id},
            requestkwargs={
                'data': {
                    'text': 'This is a comment',
                }
            })
        self.assertEquals(2, group_models.FeedbackSet.objects.count())
        last_feedbackset = group_models.FeedbackSet.objects.all()[1]
        self.assertEquals(last_feedbackset, testfeedbackset)
        self.assertEquals(1, group_models.GroupComment.objects.count())
        posted_comment = group_models.GroupComment.objects.all()[0]
        self.assertEquals(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS,
                          posted_comment.visibility)
        self.assertEquals('This is a comment', posted_comment.text)

    def test_post_new_attempt_published_comment_with_text(self):
        testgroup = mommy.make('core.AssignmentGroup')
        testfeedbackset = group_mommy.feedbackset_new_attempt_published(group=testgroup)
        examiner = mommy.make('core.Examiner', assignmentgroup=testgroup)
        self.mock_http302_postrequest(
            cradmin_role=testgroup,
            requestuser=examiner.relatedexaminer.user,
            viewkwargs={'pk': testgroup.id},
            requestkwargs={
                'data': {
                    'text': 'This is a comment',
                }
            })
        self.assertEquals(2, group_models.FeedbackSet.objects.count())
        last_feedbackset = group_models.FeedbackSet.objects.all()[1]
        self.assertEquals(last_feedbackset, testfeedbackset)
        self.assertEquals(1, group_models.GroupComment.objects.count())
        posted_comment = group_models.GroupComment.objects.all()[0]
        self.assertEquals(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS,
                          posted_comment.visibility)
        self.assertEquals('This is a comment', posted_comment.text)


class TestFeedbackfeedPublicDiscussFileUploadExaminer(TestCase,
                                                      test_feedbackfeed_examiner.TestFeedbackfeedExaminerMixin):
    viewclass = feedbackfeed_examiner.ExaminerPublicDiscussView

    def setUp(self):
        AssignmentGroupDbCacheCustomSql().initialize()

    def test_comment_without_text_or_file_visibility_everyone(self):
        # Tests that error message pops up if trying to post a comment without either text or file.
        # Posting comment with visibility visible to everyone
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.Examiner', assignmentgroup=testfeedbackset.group)
        mockresponse = self.mock_http200_postrequest_htmls(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                    'examiner_add_public_comment': 'unused value'
                }
            })
        self.assertEquals(0, group_models.GroupComment.objects.count())
        self.assertEqual(
            'A comment must have either text or a file attached, or both. An empty comment is not allowed.',
            mockresponse.selector.one('#error_1_id_text').alltext_normalized)

    def test_upload_single_file_visibility_everyone(self):
        # Test that a CommentFile is created on upload.
        # Posting comment with visibility visible to everyone
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        temporary_filecollection = group_mommy.temporary_file_collection_with_tempfile(
            user=testexaminer.relatedexaminer.user)
        self.mock_http302_postrequest(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                    'temporary_file_collection_id': temporary_filecollection.id
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        self.assertEquals(1, comment_models.CommentFile.objects.count())

    def test_upload_single_file_content_visibility_everyone(self):
        # Test the content of a CommentFile after upload.
        # Posting comment with visibility visible to everyone
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        temporary_filecollection = group_mommy.temporary_file_collection_with_tempfiles(
            file_list=[
                SimpleUploadedFile(name='testfile.txt', content=b'Test content', content_type='text/txt')
            ],
            user=testexaminer.relatedexaminer.user
        )
        self.mock_http302_postrequest(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                    'temporary_file_collection_id': temporary_filecollection.id
                }
            })
        self.assertEquals(1, comment_models.CommentFile.objects.count())
        comment_file = comment_models.CommentFile.objects.all()[0]
        group_comment = group_models.GroupComment.objects.get(id=comment_file.comment.id)
        self.assertEquals(group_comment.visibility, group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
        self.assertEquals('testfile.txt', comment_file.filename)
        self.assertEquals('Test content', comment_file.file.file.read())
        self.assertEquals(len('Test content'), comment_file.filesize)
        self.assertEquals('text/txt', comment_file.mimetype)

    def test_upload_multiple_files_visibility_everyone(self):
        # Test the content of CommentFiles after upload.
        # Posting comment with visibility visible to everyone
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        temporary_filecollection = group_mommy.temporary_file_collection_with_tempfiles(
            file_list=[
                SimpleUploadedFile(name='testfile1.txt', content=b'Test content1', content_type='text/txt'),
                SimpleUploadedFile(name='testfile2.txt', content=b'Test content2', content_type='text/txt'),
                SimpleUploadedFile(name='testfile3.txt', content=b'Test content3', content_type='text/txt')
            ],
            user=testexaminer.relatedexaminer.user
        )
        self.mock_http302_postrequest(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                    'temporary_file_collection_id': temporary_filecollection.id
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        self.assertEqual(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE,
                         group_models.GroupComment.objects.all()[0].visibility)
        self.assertEquals(3, comment_models.CommentFile.objects.count())

    def test_upload_multiple_files_contents_visibility_everyone(self):
        # Test the content of a CommentFile after upload.
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        temporary_filecollection = group_mommy.temporary_file_collection_with_tempfiles(
            file_list=[
                SimpleUploadedFile(name='testfile1.txt', content=b'Test content1', content_type='text/txt'),
                SimpleUploadedFile(name='testfile2.txt', content=b'Test content2', content_type='text/txt'),
                SimpleUploadedFile(name='testfile3.txt', content=b'Test content3', content_type='text/txt')
            ],
            user=testexaminer.relatedexaminer.user
        )
        self.mock_http302_postrequest(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                    'temporary_file_collection_id': temporary_filecollection.id
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        self.assertEqual(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE,
                         group_models.GroupComment.objects.all()[0].visibility)
        self.assertEquals(3, comment_models.CommentFile.objects.count())
        comment_file1 = comment_models.CommentFile.objects.get(filename='testfile1.txt')
        comment_file2 = comment_models.CommentFile.objects.get(filename='testfile2.txt')
        comment_file3 = comment_models.CommentFile.objects.get(filename='testfile3.txt')

        # Check content of testfile 1.
        self.assertEqual('testfile1.txt', comment_file1.filename)
        self.assertEqual('Test content1', comment_file1.file.file.read())
        self.assertEqual(len('Test content1'), comment_file1.filesize)
        self.assertEqual('text/txt', comment_file1.mimetype)

        # Check content of testfile 2.
        self.assertEqual('testfile2.txt', comment_file2.filename)
        self.assertEqual('Test content2', comment_file2.file.file.read())
        self.assertEqual(len('Test content2'), comment_file2.filesize)
        self.assertEqual('text/txt', comment_file2.mimetype)

        # Check content of testfile 3.
        self.assertEqual('testfile3.txt', comment_file3.filename)
        self.assertEqual('Test content3', comment_file3.file.file.read())
        self.assertEqual(len('Test content3'), comment_file3.filesize)
        self.assertEqual('text/txt', comment_file3.mimetype)

    def test_upload_files_and_comment_text(self):
        # Test the content of a CommentFile after upload.
        testfeedbackset = group_mommy.feedbackset_first_attempt_published()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        temporary_filecollection = group_mommy.temporary_file_collection_with_tempfiles(
            file_list=[
                SimpleUploadedFile(name='testfile1.txt', content=b'Test content1', content_type='text/txt'),
                SimpleUploadedFile(name='testfile2.txt', content=b'Test content2', content_type='text/txt'),
            ],
            user=testexaminer.relatedexaminer.user
        )
        self.mock_http302_postrequest(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': 'Test comment',
                    'temporary_file_collection_id': temporary_filecollection.id
                }
            })
        self.assertEquals(2, comment_models.CommentFile.objects.count())
        self.assertEqual(1, group_models.GroupComment.objects.count())
        group_comments = group_models.GroupComment.objects.all()
        self.assertEquals('Test comment', group_comments[0].text)


class TestFeedbackfeedExaminerWithAdminDiscussFileUpload(TestCase,
                                                         test_feedbackfeed_examiner.TestFeedbackfeedExaminerMixin):
    viewclass = feedbackfeed_examiner.ExaminerWithAdminsDiscussView

    def setUp(self):
        AssignmentGroupDbCacheCustomSql().initialize()

    def test_comment_without_text_or_file_visibility_examiners_and_admins(self):
        # Tests that error message pops up if trying to post a comment without either text or file.
        # Posting comment with visibility for examiners and admins only
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        mockresponse = self.mock_http200_postrequest_htmls(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                }
            })
        self.assertEquals(0, group_models.GroupComment.objects.count())
        self.assertEqual(
            'A comment must have either text or a file attached, or both. An empty comment is not allowed.',
            mockresponse.selector.one('#error_1_id_text').alltext_normalized)

    def test_upload_single_file_visibility_examiners_and_admins(self):
        # Test that a CommentFile is created on upload.
        # Posting comment with visibility visible to examiners and admins
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        temporary_filecollection = group_mommy.temporary_file_collection_with_tempfile(
            user=testexaminer.relatedexaminer.user)
        self.mock_http302_postrequest(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                    'temporary_file_collection_id': temporary_filecollection.id
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        self.assertEqual(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS,
                         group_models.GroupComment.objects.all()[0].visibility)
        self.assertEquals(1, comment_models.CommentFile.objects.count())

    def test_upload_single_file_content_visibility_examiners_and_admins(self):
        # Test the content of a CommentFile after upload.
        # Posting comment with visibility visible to examiners and admins
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        temporary_filecollection = group_mommy.temporary_file_collection_with_tempfiles(
            file_list=[
                SimpleUploadedFile(name='testfile.txt', content=b'Test content', content_type='text/txt')
            ],
            user=testexaminer.relatedexaminer.user
        )
        self.mock_http302_postrequest(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                    'temporary_file_collection_id': temporary_filecollection.id
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        self.assertEqual(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS,
                         group_models.GroupComment.objects.all()[0].visibility)
        self.assertEquals(1, comment_models.CommentFile.objects.count())
        comment_file = comment_models.CommentFile.objects.all()[0]
        self.assertEqual('testfile.txt', comment_file.filename)
        self.assertEqual('Test content', comment_file.file.file.read())
        self.assertEqual(len('Test content'), comment_file.filesize)
        self.assertEqual('text/txt', comment_file.mimetype)

    def test_upload_multiple_files_visibility_examiners_and_admins(self):
        # Test the content of CommentFiles after upload.
        # Posting comment with visibility visible to everyone
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        temporary_filecollection = group_mommy.temporary_file_collection_with_tempfiles(
            file_list=[
                SimpleUploadedFile(name='testfile1.txt', content=b'Test content1', content_type='text/txt'),
                SimpleUploadedFile(name='testfile2.txt', content=b'Test content2', content_type='text/txt'),
                SimpleUploadedFile(name='testfile3.txt', content=b'Test content3', content_type='text/txt')
            ],
            user=testexaminer.relatedexaminer.user
        )
        self.mock_http302_postrequest(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                    'examiner_add_comment_for_examiners': 'unused value',
                    'temporary_file_collection_id': temporary_filecollection.id
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        self.assertEqual(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS,
                         group_models.GroupComment.objects.all()[0].visibility)
        self.assertEquals(3, comment_models.CommentFile.objects.count())

    def test_upload_multiple_files_contents_visibility_examiners_and_admins(self):
        # Test the content of a CommentFile after upload.
        testfeedbackset = group_mommy.feedbackset_first_attempt_unpublished()
        testexaminer = mommy.make('core.examiner', assignmentgroup=testfeedbackset.group)
        temporary_filecollection = group_mommy.temporary_file_collection_with_tempfiles(
            file_list=[
                SimpleUploadedFile(name='testfile1.txt', content=b'Test content1', content_type='text/txt'),
                SimpleUploadedFile(name='testfile2.txt', content=b'Test content2', content_type='text/txt'),
                SimpleUploadedFile(name='testfile3.txt', content=b'Test content3', content_type='text/txt')
            ],
            user=testexaminer.relatedexaminer.user
        )
        self.mock_http302_postrequest(
            cradmin_role=testexaminer.assignmentgroup,
            requestuser=testexaminer.relatedexaminer.user,
            viewkwargs={'pk': testfeedbackset.group.id},
            requestkwargs={
                'data': {
                    'text': '',
                    'examiner_add_comment_for_examiners': 'unused value',
                    'temporary_file_collection_id': temporary_filecollection.id
                }
            })
        self.assertEquals(1, group_models.GroupComment.objects.count())
        self.assertEqual(group_models.GroupComment.VISIBILITY_VISIBLE_TO_EXAMINER_AND_ADMINS,
                         group_models.GroupComment.objects.all()[0].visibility)
        self.assertEquals(3, comment_models.CommentFile.objects.count())
        comment_file1 = comment_models.CommentFile.objects.get(filename='testfile1.txt')
        comment_file2 = comment_models.CommentFile.objects.get(filename='testfile2.txt')
        comment_file3 = comment_models.CommentFile.objects.get(filename='testfile3.txt')

        # Check content of testfile 1.
        self.assertEqual('testfile1.txt', comment_file1.filename)
        self.assertEqual('Test content1', comment_file1.file.file.read())
        self.assertEqual(len('Test content1'), comment_file1.filesize)
        self.assertEqual('text/txt', comment_file1.mimetype)

        # Check content of testfile 2.
        self.assertEqual('testfile2.txt', comment_file2.filename)
        self.assertEqual('Test content2', comment_file2.file.file.read())
        self.assertEqual(len('Test content2'), comment_file2.filesize)
        self.assertEqual('text/txt', comment_file2.mimetype)

        # Check content of testfile 3.
        self.assertEqual('testfile3.txt', comment_file3.filename)
        self.assertEqual('Test content3', comment_file3.file.file.read())
        self.assertEqual(len('Test content3'), comment_file3.filesize)
        self.assertEqual('text/txt', comment_file3.mimetype)