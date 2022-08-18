


from rest_framework import serializers
from .models import your_hobby

class your_hobbySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'your_MBTI',
            'category',
            'first_point',
            'second_point',
            'third_point',
            'return_hobby',
        )
        model = your_hobby