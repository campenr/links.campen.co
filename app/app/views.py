from django.views.generic import ListView

from app.models import Link


class Index(ListView):
    model = Link
    template_name = 'app/index.html'
    context_object_name = 'links'
