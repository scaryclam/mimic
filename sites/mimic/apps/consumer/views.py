from django.views import generic
from django.template import Template, Context
from django.http import HttpResponse, Http404

from apps.consumer.services import ConsumerService


class ConsumerView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        service = ConsumerService()
        consumer = service.get_consumer_from_path(request.path)
        # The extra published check is necessary because our use of
        # pages as categories is not what barebones was built for
        if not consumer:
            raise Http404
        context = Context(service.get_consumer_context_data(request, consumer))
        template = Template(consumer.expected_template)
        rendered = template.render(context)

        return HttpResponse(rendered)

