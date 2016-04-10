import uuid

from django.utils import timezone

from apps.agent.models import Agent


class AgentService(object):
    def register_agent(self, accepted_job_types):
        agent_id = str(uuid.uuid4())
        self.create_agent(agent_id, accepted_job_types)
        return agent_id

    def check_agent_id(self, agent_id):
        try:
            agent = Agent.objects.get(
                agent_id=agent_id,
                is_active=True)
            if not agent.is_active:
                self.set_agent_active()
        except Agent.DoesNotExist:
            return False

        return agent

    def set_agent_active(self, agent):
        agent.is_active = True
        agent.last_checkin_datetime = timezone.now()
        agent.save()

    def create_agent(self, agent_id, accepted_job_types=None):
        if not accepted_job_types:
            accepted_job_types = []

        agent = Agent.objects.create(
            agent_id=agent_id,
            registered_datetime=timezone.now(),
            last_checkin_datetime=timezone.now(),
            is_active=True)

        for job_type in accepted_job_types:
            agent.accepted_job_types.add(job_type)

        return agent

    def get_agent_by_agent_id(self, agent_id):
        try:
            agent = Agent.objects.get(agent_id=agent_id)
        except Agent.DoesNotExist:
            raise
        return agent
