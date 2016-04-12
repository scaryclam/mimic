from django.db import models


class Consumer(models.Model):
    name = models.CharField(max_length=255)
    consumer_type = models.CharField(max_length=100)
    expected_template = models.TextField(null=True, blank=True)
    frequency_limit = models.IntegerField(null=True, blank=True)
    endpoint = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return "%s for %s" % (self.name, self.endpoint)
