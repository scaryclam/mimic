import uuid
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from apps.job.models import Job, JobType


class JobService(object):
    def get_available_producer_jobs(self, agent):
        time_now = timezone.now()

        jobs = Job.objects.filter(Q(agent=None) | Q(agent=agent))\
                          .filter(job_type=agent.accepted_job_types.all())

        filter_out = []

        for job in jobs:
            job_agent = job.agent

            check_release = job.last_released and job.max_assign_freq

            if check_release and (time_now - job.last_released).total_seconds() <= job.max_assign_freq:
                filter_out.append(job.pk)
                continue

            if not job_agent or not job_agent.agent_id == agent.agent_id:
                self.set_agent(job, agent)

        jobs = jobs.exclude(pk__in=filter_out)

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

    def get_job_by_job_id(self, job_id):
        job = Job.objects.get(job_id=job_id)
        return job

    def release_job(self, job_id):
        job = self.get_job_by_job_id(job_id)
        job.agent = None
        job.last_released = timezone.now()
        job.save()
