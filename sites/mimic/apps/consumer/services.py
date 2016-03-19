from apps.consumer.models import Consumer


class ConsumerService(object):
    def get_consumer_from_path(self, path):
        try:
            return Consumer.objects.get(endpoint=path)
        except Consumer.DoesNotExist:
            return

    def get_consumer_context_data(self, request, consumer):
        return {}

