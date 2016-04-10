from django.db import models


class Agent(models.Model):
    agent_id = models.CharField(max_length=200)
    registered_datetime = models.DateTimeField(null=True, blank=True)
    last_checkin_datetime = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    accepted_job_types = models.ManyToManyField(
        'job.JobType', null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.agent_id)
