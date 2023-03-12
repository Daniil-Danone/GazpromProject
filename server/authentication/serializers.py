from rest_framework import serializers
from .models import GazpromUser, Well, Check


class GazpromUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GazpromUser
        fields = ('login', 'name', 'surname')


class GazpromUserSerializer(serializers.Serializer):  # преобразование типов данных для модели GazpromUser
    login = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=255, required=True)
    name = serializers.CharField(allow_blank=True, required=False)
    surname = serializers.CharField(allow_blank=True, required=False)
    isAdmin = serializers.BooleanField(default=False)
    isDeveloper = serializers.BooleanField(default=False)
    isLogin = serializers.BooleanField(read_only=True)
    joined_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    token = serializers.CharField(allow_blank=True, required=False)

    def create(self, validated_data):
        return GazpromUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = "__all__"


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"
