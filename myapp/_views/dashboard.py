from django.urls import reverse_lazy
from myapp.mixins.ajax import AjaxTemplateMixin

class DashboardView(AjaxTemplateMixin):
    """
    Renders the user dashboard with AJAX support.

    - Full page: loads layout, assets, user context
    - AJAX: returns only the content fragment
    """
    # Full-page template (used on initial load or non-AJAX requests)
    template_name = 'sessions/dashboard_full.html'
    
    # AJAX fragment template (used when JS requests only the inner HTML)
    ajax_template_name = 'sessions/dashboard_fragment.html'

    # URL to redirect to on successful form submissions or redirects
    success_url = reverse_lazy('profile:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any needed data for the dashboard, e.g. recent activity
        context['recent_items'] = self.get_recent_items()
        return context

    def get_recent_items(self):
        # Example: fetch last 5 user actions
        return self.request.user.actions.order_by('-timestamp')[:5]
