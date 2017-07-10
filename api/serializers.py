from rest_framework import serializers
from .models import Duckling, Quack

class QuackSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format"""

    submitted_by = serializers.ReadOnlyField(source='submitted_by.username')

    class Meta:
	"""Meta class to map serializer's fields with the model fields."""
	model = Quack
	fields = ('id', 'message', 'submitted_by', 'submit_date', 'has_been_processed', 'is_approved')
        read_only_fields = ('submit_date', 'has_been_processed', 'is_approved')
 
