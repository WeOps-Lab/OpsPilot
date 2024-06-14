from rest_framework import serializers


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text="用户名")
    password = serializers.CharField(required=True, help_text="密码")
