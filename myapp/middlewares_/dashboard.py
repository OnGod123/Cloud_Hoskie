# myapp/profile/views.py

from django.views.generic import TemplateView
from .mixins import AjaxTemplateMixin

class DashboardView(AjaxTemplateMixin, TemplateView):
    template_name = 'profile/dashboard_full.html'
    ajax_template_name = 'profile/dashboard_fragment.html'

