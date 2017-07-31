from rest_framework import serializers
from .models import Duckling, Quack
from django.contrib.auth.models import User

class QuackSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format"""

    submitted_by = serializers.ReadOnlyField(source='submitted_by.username')

    class Meta:
	"""Meta class to map serializer's fields with the model fields."""
	model = Quack
	fields = ('id', 'message', 'submitted_by', 'submit_date', 'has_been_processed', 'is_approved')
        read_only_fields = ('submit_date', 'has_been_processed', 'is_approved')
 

class DucklingSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format"""

    user = serializers.ReadOnlyField(source = 'user.username')
    notification_schedule = serializers.ReadOnlyField(source = 'notification_schedule.id')
    is_moderator = serializers.ReadOnlyField(required=False)    
    #quack_list = serializers.ReadOnlyField(source = 'quack.id')

    class Meta:
	model = Duckling
	fields = '__all__'
	read_only_fields = ('user', 'notification_schedule', 'is_moderator', 'quack_list')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
	model = User
	fields = ('username', 'email', 'password')
	write_only_fields= ('password',)
    
    def create(self, validated_data):
	user = User.objects.create(
	    username = validated_data['username']
	)
	user.set_password(validated_data['password'])
	user.save()
        return user

