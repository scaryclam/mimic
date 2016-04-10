import json

from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse

from apps.agent.services import AgentService
from apps.job.services import JobService


class AgentRegisterView(View):
    def post(self, request, *args, **kwargs):
        job_service = JobService()
        agent_job_types = request.POST.getlist('job_types', [])
        job_types = []
        for job_type_name in agent_job_types:
            job_type = job_service.get_job_type_by_name(job_type_name)
            if not job_type:
                continue
            else:
                job_types.append(job_type)
        agent_uuid = AgentService().register_agent(job_types)
        agent_response_data = {'identifier': agent_uuid}
        return HttpResponse(json.dumps(agent_response_data))


class AgentJobsRequestView(View):
    def get(self, request, *args, **kwargs):
        agent_id = request.META.get('HTTP_AGENT_ID', None)
        if not agent_id:
            # There was no agent idenitifier, tell the agent to go register
            agent_response_data = {'resolution': "register",
                                   'next': reverse('agent:register'),
                                   'reason': "No agent ID found"}
            return HttpResponseForbidden(json.dumps(agent_response_data))

        try:
            agent = AgentService().check_agent_id(agent_id)
        except:
            agent_response_data = {'resolution': "register",
                                   'next': reverse('agent:register'),
                                   'reason': "No valid agent found"}
            return HttpResponseForbidden(json.dumps(agent_response_data))
        if not agent:
            agent_response_data = {'resolution': "register",
                                   'next': reverse('agent:register'),
                                   'reason': "No valid agent found"}
            return HttpResponseForbidden(json.dumps(agent_response_data))

        assigned_jobs = JobService().get_available_producer_jobs(agent)

        jobs = []

        for job in assigned_jobs:
            jobs.append({'name': job.name})

        agent_response_data = {'jobs': jobs}
        return HttpResponse(json.dumps(agent_response_data))
