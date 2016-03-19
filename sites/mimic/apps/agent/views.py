from django.views.generic import View
from django.http import HttpResponse


class AgentRegisterView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse("{}")

    def get(self, request, *args, **kwargs):
        return HttpResponse("ssss")
