Ext.define('devilry_header.AdminSearchResultsView', {
    extend: 'devilry_header.BaseSearchResultsView',
    alias: 'widget.devilry_header_adminsearchresults',
    extraCls: 'devilry_header_adminsearchresults',

    singleResultTpl: [
        '<div><a href="#"><strong class="title">{title}</strong></a> <small>({type})</small></div>',
        '<div class="muted"><small class="path">{path}</small></div>'
    ],

    heading: gettext('Content where you are admin')
});