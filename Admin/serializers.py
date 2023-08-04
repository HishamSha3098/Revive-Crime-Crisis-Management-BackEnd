from rest_framework import serializers
from .models import CrisisManage,EventManage,GalleryManage
from django.core.exceptions import ValidationError


class CrisisManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisManage
        fields = ['id','user', 'title', 'description', 'image', 'donation_goal', 'recived_amount', 'date_time', 'document', 'is_active']

    def create(self, validated_data):
        # Create a new crisis instance using the validated data
        crisis = CrisisManage.objects.create(**validated_data)
        return crisis

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.donation_goal = validated_data.get('donation_goal', instance.donation_goal)
        instance.recived_amount = validated_data.get('recived_amount', instance.recived_amount)
        instance.date_time = validated_data.get('date_time', instance.date_time)
        instance.document = validated_data.get('document', instance.document)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
    


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventManage
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryManage
        fields = '__all__'





