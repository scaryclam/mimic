import json

from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse

from apps.agent.services import AgentService
from apps.job.services import JobService


class JobReleaseView(View):
    def post(self, request, *args, **kwargs):
        job_service = JobService()
        job_id = request.POST['job_id']
        job_service.release_job(job_id)

        response_data = {'status': 'success'}
        return HttpResponse(json.dumps(response_data))
