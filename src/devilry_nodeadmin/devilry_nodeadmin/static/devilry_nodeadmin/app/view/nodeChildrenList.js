Ext.define('devilry_nodeadmin.view.nodeChildrenList', {
    extend: 'Ext.view.View',
    alias: 'widget.nodechildrenlist',
    cls: 'bootstrap',
    tpl: [
        '<div class="bootstrap">',
        '<tpl if="length">',
            '<h2>Noden inneholder</h2>',
        '<tpl else>',
            '<h2><small>ingen noder</small></h2>',
        '</tpl>',
        '<tpl for=".">',
        '<div style="padding-bottom: 10px;">',
            '<a href="/devilry_nodeadmin/#/node/{ id }"><h3>',
                '<tpl for="predecessor">{ short_name }</tpl>',
            ' / { long_name }</h3>',
            '<tpl if="most_recent_start_time != null">',
                '<div>Earliest start time: { most_recent_start_time }</div>',
            '<tpl else>',
                '<div>Earliest start time: none</div>',
            '</tpl>',
            '</a>',
        '</div>',
        '</tpl>',
        '</div>'
    ],

    itemSelector: 'div.node',

    initComponent: function() {
        this.store = Ext.create( 'devilry_nodeadmin.store.NodeChildren' );
        this.store.proxy.url = Ext.String.format('/devilry_nodeadmin/rest/node/{0}/children', this.node_pk );
        this.callParent(arguments);
    }

});