Ext.application({
    name: 'subjectadmin',
    appFolder: DevilrySettings.DEVILRY_STATIC_URL + '/subjectadmin/app',

    requires: [
        'guibase.RouteNotFound',
        'themebase.view.Breadcrumbs'
    ],

    controllers: [
        'ShortcutsTestMock',
        'Dashboard',
        'CreateNewAssignmentTestMock',
        'ChoosePeriodTestMock'
    ],

    launch: function() {
        this.breadcrumbs = Ext.widget('breadcrumbs', {
            region: 'north',
            //height: 30
        });
        this.contentContainer = Ext.widget('container', {
            region: 'center',
            layout: 'fit'
        });
        this.viewport = Ext.create('Ext.container.Viewport', {
            layout: 'border',
            items: [this.breadcrumbs, this.contentContainer]
        });
        this.route = Ext.create('guibase.Router', this);
        this.route.add("", 'dashboard');
        this.route.add("/@@create-new-assignment/@@chooseperiod", 'create_new_assignment_chooseperiod');
        this.route.add("/@@create-new-assignment/:period", 'create_new_assignment');
        //this.route.add("/:subject/:period", 'period_show');
        //this.route.add("/:subject/:period/@@edit", 'period_edit');
        //this.route.add("/:subject/:period/:assignment", 'assignment_show');

        // These views are only for unit tests
        this.route.add("/@@dashboard/shortcutlist", 'shortcutlist');
        this.route.add("/@@dashboard/actionlist", 'actionlist');
        this.route.start();
    },

    routeNotFound: function(route) {
        this.setView({
            xtype: 'routenotfound',
            data: {
                route: route.token
            }
        });
    },

    setView: function(component) {
        this.contentContainer.removeAll();
        this.contentContainer.add(component);
    },


    /*********************************************
     * Moch the actual interface
     ********************************************/
    dashboard: function() {
        this.breadcrumbs.setHome();
        this.setView({
            xtype: 'dashboard'
        });
    },

    create_new_assignment_chooseperiod: function(info) {
        this.breadcrumbs.set([], translate('subjectadmin.chooseperiod.title'));
        this.setView({
            xtype: 'chooseperiod',
            nexturlformat: '/@@create-new-assignment/{0}'
        });
    },

    create_new_assignment: function(info, periodId) {
        this.breadcrumbs.set([], translate('subjectadmin.createnewassignment.title'));
        this.setView({
            xtype: 'createnewassignment',
            periodId: periodId
        });
    },

    //period_show: function(route, subject, period) {
        //console.log('PE', route, subject, period);
    //},
    //period_edit: function(route, subject, period) {
        //console.log(route, subject, period);
    //},

    //assignment_show: function(route, subject, period, assignment) {
        //console.log('Assignment', subject, period, assignment);
    //},

    /*********************************************
     * Only for testing.
     ********************************************/
    shortcutlist: function() {
        this.setView({xtype: 'shortcutlist'});
    },

    actionlist: function() {
        this.setView({
            xtype: 'actionlist',
            data: {
                title: 'Action list test',
                links: [{
                    url: '#/@@actionitem-1',
                    text: 'Action item 1'
                }, {
                    url: '#/@@actionitem-2',
                    text: 'Action item 2'
                }]
            }
        });
    }
});
