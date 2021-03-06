from django_cradmin.viewhelpers import listbuilder


class GoForwardLinkItemFrame(listbuilder.itemframe.Link):
    template_name = 'devilry_cradmin/common/goforwardlinkitemframe.django.html'

    def get_base_css_classes_list(self):
        cssclasses = super(GoForwardLinkItemFrame, self).get_base_css_classes_list()
        cssclasses.append('devilry-django-cradmin-listbuilder-itemframe-goforward')
        return cssclasses
