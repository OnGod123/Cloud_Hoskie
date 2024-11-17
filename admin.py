from django.contrib import admin
from myapp.models import Person
from myapp.video_call.models import VideoCall, CallParticipants, CallMetrics

admin.site.register(Person)
admin.site.register(VideoCall)
admin.site.register(CallParticipants)
admin.site.register(CallMetrics)
