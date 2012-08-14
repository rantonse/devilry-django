from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.i18n import javascript_catalog
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from views import AppView

i18n_packages = ('devilry_student', 'devilry_extjsextras')

urlpatterns = patterns('devilry_subjectadmin',
                       url('^$', login_required(csrf_protect(ensure_csrf_cookie(AppView.as_view()))),
                           name='devilry_student'),
                       url('^rest/', include('devilry_student.rest.urls')),
                       url('^i18n.js$', javascript_catalog, kwargs={'packages': i18n_packages},
                           name='devilry_student_i18n'))
