from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=255)
    agent = models.ForeignKey('agent.Agent', null=True, blank=True)
    job_type = models.ForeignKey('job.JobType')

    def __unicode__(self):
        agent_str = self.agent.agent_id if self.agent else "No Agent Assigned"
        return "%s (Agent: %s)" % (self.name, agent_str)


class JobType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name


class JobTypeMeta(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=512)
    job_type = models.ForeignKey('job.JobType')

    def __unicode__(self):
        agent_str = self.agent.agent_id if self.agent else "No Agent Assigned"
        return "%s - %s (%s)" % (self.key, self.value, self.job_type)
