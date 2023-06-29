from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from . import models

class MenuSerializer(ModelSerializer):
    class Meta:
        model = models.Menu
        fields = "__all__"


class BookingSerializer(ModelSerializer):
    class Meta:
        model = models.Booking
        fields = "__all__"



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
