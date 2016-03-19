from django.db import models


class Producer(models.Model):
    name = models.CharField(max_length=255)
    producer_type = models.CharField(max_length=100)
    output_template = models.TextField()
    frequency = models.IntegerField(null=True, blank=True)
#    outputs
#
#
#class ProducerPlaybook(models.Model):



