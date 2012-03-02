/**
 * Success page for CreateNewAssignment.
 */
Ext.define('subjectadmin.view.createnewassignment.SuccessPanel' ,{
    extend: 'Ext.panel.Panel',
    alias: 'widget.createnewassignment-successpanel',
    requires: [
        'subjectadmin.view.ActionList',
        'Ext.XTemplate'
    ],
    cls: 'createnewassignment-successpanel',

    bodyPadding: 40,
    autoScroll: true,
    items: [{
        xtype: 'box',
        itemId: 'header'
    }],

    headertemplate: [
        '<h2>{title}</h2>',
    ],


    initComponent: function() {
        this.callParent(arguments);
    },

    /**
     * The ``config`` parameter must have the following attributes:
     *
     * subject_short_name (required)
     *      The ``short_name`` of the subject where the assignment was created.
     * period_short_name (required)
     *      The ``short_name`` of the period where the assignment was created.
     * short_name (required)
     *      The ``short_name`` of the created assignment.
     * period_id (required)
     *      The ``id`` of the period where the assignment was created.
     */
    setup: function(config) {
        var period = Ext.String.format('{0}.{1}',
            config.subject_short_name, config.period_short_name
        );
        var assignment = Ext.String.format('{0}.{1}',
            period, config.short_name
        );
        var title = Ext.create('Ext.XTemplate', dtranslate('subjectadmin.createnewassignment.success.title')).apply({
            assignment: assignment
        })
        var header = Ext.create('Ext.XTemplate', this.headertemplate).apply({
            title: title
        });
        this.down('#header').update(header);

        var gotoText = Ext.create('Ext.XTemplate', dtranslate('subjectadmin.createnewassignment.success.gotocreated')).apply({
            assignment: assignment
        });

        var type;
        if(this.delivery_types == 0) {
            type = dtranslate('subjectadmin.assignment.delivery_types.electronic');
        } else {
            type = dtranslate('subjectadmin.assignment.delivery_types.nonelectronic');
        }
        var another_similarText = Ext.create('Ext.XTemplate', dtranslate('subjectadmin.createnewassignment.success.addanother_similar')).apply({
            period: period,
            deliverytype: type
        });

        var links = [{
            url: Ext.String.format(
                '#/{0}/{1}/{2}',
                config.subject_short_name,
                config.period_short_name,
                config.short_name
            ),
            text: gotoText
        }, {
            url: '#/@@create-new-assignment/@@chooseperiod',
            buttonType: 'default',
            buttonSize: 'normal',
            text: dtranslate('subjectadmin.createnewassignment.success.addanother')
        }, {
            url: Ext.String.format(
                '#/@@create-new-assignment/{0},{1}',
                config.period_id, config.delivery_types
            ),
            buttonType: 'default',
            buttonSize: 'normal',
            text: another_similarText
        }]
        this.add({
            xtype: 'actionlist',
            margin: {top: 20},
            width: 460,
            linkStyle: 'width: 100%',
            links: links
        });
    }
});
