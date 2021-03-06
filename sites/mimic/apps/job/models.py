from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=255)
    agent = models.ForeignKey('agent.Agent', null=True, blank=True)
    job_type = models.ForeignKey('job.JobType')
    job_id = models.CharField(max_length=255, unique=True)
    last_released = models.DateTimeField(null=True, blank=True)
    max_assign_freq = models.PositiveIntegerField(
        null=True, blank=True, default=0,
        help_text="Time, in seconds, that this job will NOT be reassigned for after release")

    def __unicode__(self):
        agent_str = self.agent.agent_id if self.agent else "No Agent Assigned"
        return "%s (Agent: %s)" % (self.name, agent_str)


class JobType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name


class JobMeta(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=512)
    job = models.ForeignKey('job.Job')

    def __unicode__(self):
        return "%s - %s (%s)" % (self.key, self.value, self.job)
