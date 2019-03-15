from django.db import models
from hbook.users.models import User2
from rest_framework.serializers import HyperlinkedModelSerializer

class Appointment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(User2, on_delete=models.CASCADE, related_name="created_appointments")
    details = models.TextField(blank=True, null=True)
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField()


class AppointmentRegister(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="registered_users")
    registered_user = models.ForeignKey(User2, on_delete=models.CASCADE, related_name="registered_appointments")
    details=models.TextField(blank=True, null=True)
    line_index = models.PositiveIntegerField()
    approx_time = models.DateTimeField()
    status = models.SmallIntegerField(default=0)
    time_utilized=models.PositiveIntegerField(default=0)

    # 0 = waiting, 1 = processing, 2 = canceled, 3 = completed


class AppointmentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Appointment
        fields = ('pk', 'url', 'name', 'creator', 'details', 'time_begin', 'time_end', 'registered_users')

class AppointmentRegisterSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AppointmentRegister
        fields = ('pk', 'url', 'appointment', 'registered_user', 'details', 'line_index', 'approx_time', 'status', 'time_utilized')



