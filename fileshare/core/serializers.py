from rest_framework import serializers
from .models import User, FileUpload
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'uploaded_at']
    def validate_file(self, value):
        valid_extensions = ['.docx', '.xlsx', '.pptx']
        import os
        ext = os.path.splitext(value.name)[1]
        if ext.lower() not in valid_extensions:
            raise serializers.ValidationError('Unsupported file type.')
        return value
