from django.db import models
from myapp.models import Person

class VideoCall(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('ended', 'Ended'),
        ('missed', 'Missed'),
        ('scheduled', 'Scheduled'),
    ]

    initiator = models.ForeignKey(Person, related_name='initiated_calls', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Person, related_name='received_calls', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"Call from {self.initiator} to {self.recipient} at {self.start_time}"

class CallParticipants(models.Model):
    call = models.ForeignKey(VideoCall, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    joined_at = models.DateTimeField()
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('call', 'person')

    def __str__(self):
        return f"{self.person} in call {self.call.call_id}"

class CallMetrics(models.Model):
    CONNECTION_STRENGTH_CHOICES = [
        ('poor', 'Poor'),
        ('fair', 'Fair'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    ]

    call = models.ForeignKey(VideoCall, on_delete=models.CASCADE)
    latency_ms = models.IntegerField()
    packet_loss_rate = models.FloatField()
    connection_strength = models.CharField(max_length=10, choices=CONNECTION_STRENGTH_CHOICES)
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Metrics for call {self.call.call_id} logged at {self.logged_at}"