from django.db.models import Q

from apps.job.models import Job, JobType


class JobService(object):
    def get_available_producer_jobs(self, agent):
        jobs = Job.objects.filter(Q(agent=None) | Q(agent=agent))\
                          .filter(job_type=agent.accepted_job_types.all())

        for job in jobs:
            job_agent = job.agent
            if not job_agent or not job_agent.agent_id == agent.agent_id:
                self.set_agent(job, agent)

        return jobs

    def set_agent(self, job, agent):
        job.agent = agent
        job.save()

    def get_job_type_by_name(self, name):
        try:
            job_type = JobType.objects.get(name=name)
        except JobType.DoesNotExist:
            return
        return job_type
