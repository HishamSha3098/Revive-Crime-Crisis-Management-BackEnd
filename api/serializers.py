from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import ReviveUser,Complaint,Department,StaffApplication

class ReviveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviveUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

   


class ReviveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviveUser
        fields = '__all__'




class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffApplication
        fields = '__all__'