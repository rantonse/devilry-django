/**
 * Mixin for basenode controllers that need to set the breadcrumb.
 */
Ext.define('devilry_subjectadmin.utils.BasenodeBreadcrumbMixin', {
    requires: ['devilry_subjectadmin.utils.UrlLookup'],

    _getBreadcrumbPrefix: function() {
        return [{
            text: gettext("All subjects"),
            url: '#/'
        }];
    },

    _addBasenodeBreadcrumbToBreadcrumb: function(breadcrumb, basenodeRecord, skipLast) {
        var breadcrumbList = basenodeRecord.get('breadcrumb');
        Ext.each(breadcrumbList, function(item, index) {
            var isLast = index == breadcrumbList.length-1;
            if(isLast && skipLast) {
                return false; // break;
            }
            var url = devilry_subjectadmin.utils.UrlLookup.overviewByType(item.type, item.id);
            breadcrumb.push({
                text: item.text,
                url: url
            });
        }, this);
    },

    setBreadcrumb: function(basenodeRecord) {
        var breadcrumb = this._getBreadcrumbPrefix();
        this._addBasenodeBreadcrumbToBreadcrumb(breadcrumb, basenodeRecord, true);
        var breadcrumbList = basenodeRecord.get('breadcrumb');
        var lastBreadcrumb = breadcrumbList[breadcrumbList.length-1];
        this.application.breadcrumbs.set(breadcrumb, lastBreadcrumb.text);
    },

    /** For children of basenodes */
    setSubviewBreadcrumb: function(basenodeRecord, basenodeType, extra, current) {
        var breadcrumb = this._getBreadcrumbPrefix();
        this._addBasenodeBreadcrumbToBreadcrumb(breadcrumb, basenodeRecord);
        breadcrumb.push({
            text: basenodeRecord.get('short_name'),
            url: devilry_subjectadmin.utils.UrlLookup.overviewByType(basenodeType, basenodeRecord.get('id'))
        });
        breadcrumb = breadcrumb.concat(extra);
        this.application.breadcrumbs.set(breadcrumb, current);
    },

    setLoadingBreadcrumb: function() {
        this.application.breadcrumbs.set([], gettext('Loading ...'));
    },

    getPathFromBreadcrumb: function(basenodeRecord) {
        var path = '';
        Ext.Array.each(basenodeRecord.get('breadcrumb'), function(item) {
            if(item.type === 'Node') {
                return false; // break
            }
            path = item.short_name + '.' + path;
        }, this, true);
        return path + basenodeRecord.get('short_name');
    }
});
