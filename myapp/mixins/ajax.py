from django.shortcuts import render
from django.views import View
from django.utils.functional import cached_property

class AjaxTemplateMixin(View):
    """
    Renders either a full-page template or an AJAX fragment based on request headers.

    Attributes values should be set on the view:
      - `template_name`: full-page HTML
      - `ajax_template_name`: partial fragment
    """
    ajax_header = 'HTTP_X_REQUESTED_WITH'
    ajax_header_value = 'XMLHttpRequest'

    def render_to_response(self, context, **response_kwargs):
        request = self.request
        is_ajax = request.META.get(self.ajax_header) == self.ajax_header_value
        template = self.ajax_template_name if is_ajax else self.template_name
        # Use Django's render shortcut for convenience and built-in optimizations
        return render(request, template, context, **response_kwargs)

    @cached_property
    def is_ajax_request(self):
        """
        Cached evaluation of AJAX check to avoid repeated header lookups.
        """
        return self.request.META.get(self.ajax_header) == self.ajax_header_value
