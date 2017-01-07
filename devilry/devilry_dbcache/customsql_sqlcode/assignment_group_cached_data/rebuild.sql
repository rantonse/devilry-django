set log_error_verbosity=TERSE;


-- Takes the ID of an AssignmentGroup, and returns a
-- RECORD with all the attributes for the AssignmentGroupCachedData
-- model.
--
-- The RECORD is made using a SELECT query with sub-selects for each
-- attribute. So this is a bit expensive, but not overly so.
CREATE OR REPLACE FUNCTION devilry__collect_groupcachedata(
    param_group_id integer)
RETURNS RECORD AS $$
DECLARE
    var_groupcachedata RECORD;
BEGIN
    SELECT
        (
            SELECT id
            FROM devilry_group_feedbackset AS first_feedbackset
            WHERE group_id = param_group_id
            ORDER BY deadline_datetime ASC NULLS FIRST
            LIMIT 1
        ) AS first_feedbackset_id,
        (
            SELECT id
            FROM devilry_group_feedbackset AS last_feedbackset
            WHERE group_id = param_group_id
            ORDER BY deadline_datetime DESC NULLS LAST
            LIMIT 1
        ) AS last_feedbackset_id,
        (
            SELECT id
            FROM devilry_group_feedbackset AS last_published_feedbackset
            WHERE
                group_id = param_group_id
                AND
                grading_published_datetime IS NOT NULL
            ORDER BY deadline_datetime DESC NULLS LAST
            LIMIT 1
        ) AS last_published_feedbackset_id,
        (
            SELECT COUNT(id)
            FROM devilry_group_feedbackset
            WHERE
                group_id = param_group_id
                AND
                feedbackset_type = 'new_attempt'
        ) AS new_attempt_count,
        (
            SELECT COUNT(devilry_group_groupcomment.comment_ptr_id)
            FROM devilry_group_groupcomment
            INNER JOIN devilry_group_feedbackset
                ON devilry_group_feedbackset.id = devilry_group_groupcomment.feedback_set_id
            WHERE
                devilry_group_feedbackset.group_id = param_group_id
                AND
                devilry_group_groupcomment.visibility = 'visible-to-everyone'
        ) AS public_total_comment_count,
        (
            SELECT COUNT(devilry_group_groupcomment.comment_ptr_id)
            FROM devilry_group_groupcomment
            INNER JOIN devilry_group_feedbackset
                ON devilry_group_feedbackset.id = devilry_group_groupcomment.feedback_set_id
            INNER JOIN devilry_comment_comment
                ON devilry_comment_comment.id = devilry_group_groupcomment.comment_ptr_id
            WHERE
                devilry_group_feedbackset.group_id = param_group_id
                AND
                devilry_group_groupcomment.visibility = 'visible-to-everyone'
                AND
                devilry_comment_comment.user_role = 'student'
        ) AS public_student_comment_count,
        (
            SELECT COUNT(devilry_group_groupcomment.comment_ptr_id)
            FROM devilry_group_groupcomment
            INNER JOIN devilry_group_feedbackset
                ON devilry_group_feedbackset.id = devilry_group_groupcomment.feedback_set_id
            INNER JOIN devilry_comment_comment
                ON devilry_comment_comment.id = devilry_group_groupcomment.comment_ptr_id
            WHERE
                devilry_group_feedbackset.group_id = param_group_id
                AND
                devilry_group_groupcomment.visibility = 'visible-to-everyone'
                AND
                devilry_comment_comment.user_role = 'examiner'
        ) AS public_examiner_comment_count,
        (
            SELECT COUNT(devilry_group_groupcomment.comment_ptr_id)
            FROM devilry_group_groupcomment
            INNER JOIN devilry_group_feedbackset
                ON devilry_group_feedbackset.id = devilry_group_groupcomment.feedback_set_id
            INNER JOIN devilry_comment_comment
                ON devilry_comment_comment.id = devilry_group_groupcomment.comment_ptr_id
            WHERE
                devilry_group_feedbackset.group_id = param_group_id
                AND
                devilry_group_groupcomment.visibility = 'visible-to-everyone'
                AND
                devilry_comment_comment.user_role = 'admin'
        ) AS public_admin_comment_count,
        (
            SELECT COUNT(devilry_group_imageannotationcomment.comment_ptr_id)
            FROM devilry_group_imageannotationcomment
            INNER JOIN devilry_group_feedbackset
                ON devilry_group_feedbackset.id = devilry_group_imageannotationcomment.feedback_set_id
            WHERE
                devilry_group_feedbackset.group_id = param_group_id
                AND
                devilry_group_imageannotationcomment.visibility = 'visible-to-everyone'
        ) AS public_total_imageannotationcomment_count,
        (
            SELECT COUNT(devilry_group_imageannotationcomment.comment_ptr_id)
            FROM devilry_group_imageannotationcomment
            INNER JOIN devilry_group_feedbackset
                ON devilry_group_feedbackset.id = devilry_group_imageannotationcomment.feedback_set_id
            INNER JOIN devilry_comment_comment
                ON devilry_comment_comment.id = devilry_group_imageannotationcomment.comment_ptr_id
            WHERE
                devilry_group_feedbackset.group_id = param_group_id
                AND
                devilry_group_imageannotationcomment.visibility = 'visible-to-everyone'
                AND
                devilry_comment_comment.user_role = 'student'
        ) AS public_student_imageannotationcomment_count,
        (
            SELECT COUNT(devilry_group_imageannotationcomment.comment_ptr_id)
            FROM devilry_group_imageannotationcomment
            INNER JOIN devilry_group_feedbackset
                ON devilry_group_feedbackset.id = devilry_group_imageannotationcomment.feedback_set_id
            INNER JOIN devilry_comment_comment
                ON devilry_comment_comment.id = devilry_group_imageannotationcomment.comment_ptr_id
            WHERE
                devilry_group_feedbackset.group_id = param_group_id
                AND
                devilry_group_imageannotationcomment.visibility = 'visible-to-everyone'
                AND
                devilry_comment_comment.user_role = 'examiner'
        ) AS public_examiner_imageannotationcomment_count,
        (
            SELECT COUNT(devilry_group_imageannotationcomment.comment_ptr_id)
            FROM devilry_group_imageannotationcomment
            INNER JOIN devilry_group_feedbackset
                ON devilry_group_feedbackset.id = devilry_group_imageannotationcomment.feedback_set_id
            INNER JOIN devilry_comment_comment
                ON devilry_comment_comment.id = devilry_group_imageannotationcomment.comment_ptr_id
            WHERE
                devilry_group_feedbackset.group_id = param_group_id
                AND
                devilry_group_imageannotationcomment.visibility = 'visible-to-everyone'
                AND
                devilry_comment_comment.user_role = 'admin'
        ) AS public_admin_imageannotationcomment_count
    FROM core_assignmentgroup AS assignmentgroup
    WHERE id = param_group_id
    INTO var_groupcachedata;

    RETURN var_groupcachedata;
END
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION devilry__rebuild_assignmentgroupcacheddata(
    param_group_id integer)
RETURNS VOID AS $$
DECLARE
    var_groupcachedata RECORD;
BEGIN
    var_groupcachedata = devilry__collect_groupcachedata(param_group_id);

    INSERT INTO devilry_dbcache_assignmentgroupcacheddata (
        group_id,
        first_feedbackset_id,
        last_feedbackset_id,
        last_published_feedbackset_id,
        new_attempt_count,
        public_total_comment_count,
        public_student_comment_count,
        public_examiner_comment_count,
        public_admin_comment_count,
        public_total_imageannotationcomment_count,
        public_student_imageannotationcomment_count,
        public_examiner_imageannotationcomment_count,
        public_admin_imageannotationcomment_count,
        file_upload_count_total,
        file_upload_count_student,
        file_upload_count_examiner)
    VALUES (
        param_group_id,
        var_groupcachedata.first_feedbackset_id,
        var_groupcachedata.last_feedbackset_id,
        var_groupcachedata.last_published_feedbackset_id,
        var_groupcachedata.new_attempt_count,
        var_groupcachedata.public_total_comment_count,
        var_groupcachedata.public_student_comment_count,
        var_groupcachedata.public_examiner_comment_count,
        var_groupcachedata.public_admin_comment_count,
        var_groupcachedata.public_total_imageannotationcomment_count,
        var_groupcachedata.public_student_imageannotationcomment_count,
        var_groupcachedata.public_examiner_imageannotationcomment_count,
        var_groupcachedata.public_admin_imageannotationcomment_count,
        0,  -- file_upload_count_total,
        0,  -- file_upload_count_student,
        0   -- file_upload_count_examiner
    )
    ON CONFLICT(group_id)
    DO UPDATE SET
        first_feedbackset_id = var_groupcachedata.first_feedbackset_id,
        last_feedbackset_id = var_groupcachedata.last_feedbackset_id,
        last_published_feedbackset_id = var_groupcachedata.last_published_feedbackset_id,
        new_attempt_count = var_groupcachedata.new_attempt_count,
        public_total_comment_count = var_groupcachedata.public_total_comment_count,
        public_student_comment_count = var_groupcachedata.public_student_comment_count,
        public_examiner_comment_count = var_groupcachedata.public_examiner_comment_count,
        public_admin_comment_count = var_groupcachedata.public_admin_comment_count,
        public_total_imageannotationcomment_count = var_groupcachedata.public_total_imageannotationcomment_count,
        public_student_imageannotationcomment_count = var_groupcachedata.public_student_imageannotationcomment_count,
        public_examiner_imageannotationcomment_count = var_groupcachedata.public_examiner_imageannotationcomment_count,
        public_admin_imageannotationcomment_count = var_groupcachedata.public_admin_imageannotationcomment_count,
        file_upload_count_total = 0,
        file_upload_count_student = 0,
        file_upload_count_examiner = 0;
END
$$ LANGUAGE plpgsql;
