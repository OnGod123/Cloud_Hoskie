# myapp/mixins.py

from django.shortcuts import render

class AjaxTemplateMixin:
    """
    Views using this mixin should set:
      template_name: full-page template (extends base.html)
      ajax_template_name: fragment-only template (just the #main-content block)
    """
    ajax_param = 'HTTP_X_REQUESTED_WITH'
    ajax_value = 'XMLHttpRequest'

    def render_to_response(self, context, **response_kwargs):
        request = self.request
        is_ajax = request.META.get(self.ajax_param) == self.ajax_value
        template = self.ajax_template_name if is_ajax else self.template_name
        return render(request, template, context)

