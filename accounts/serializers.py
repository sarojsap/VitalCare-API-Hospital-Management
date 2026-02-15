from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role']
    

    def create(self, validated_data):
        # Security: remove password from the dict so we can hash it later
        password = validated_data.pop('password', None)

        # Security: Prevent users from signing up as Admin via API
        if validated_data.get('role') == User.RoleOption.ADMIN:
            validated_data['role'] = User.RoleOption.PATIENT
        
        # Using the manager to create the user safely
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()

        return instance
        