Ext.define('devilry_nodeadmin.view.NodeBrowserOverview', {
    extend: 'Ext.container.Container',
    alias: 'widget.nodebrowseroverview',
    cls: 'devilry_nodeadmin_nodebrowseroverview',

    layout: 'column',
    autoScroll: true,

    /**
     * @cfg {int} [node_pk]
     */

    items: [{
        xtype: 'container',
        itemId: 'primary',
        columnWidth: 0.5,
        padding: '30 20 20 30'
//        items: [{
//            xtype: 'nodeparentlink',
//            node_pk: this.node_pk
//        }, {
//            xtype: 'nodechildrenlist',
//            node_pk: this.node_pk
//        }]
    }, {
        xtype: 'container',
        itemId: 'secondary',
        columnWidth: 0.5,
        padding: '30 20 20 30'
    }]
});