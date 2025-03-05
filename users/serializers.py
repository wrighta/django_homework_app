from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import Child
User = get_user_model()


class ChildCreationSerializer(serializers.ModelSerializer):
    child_username = serializers.CharField(write_only=True)
    child_password = serializers.CharField(write_only=True)
    parent_username = serializers.CharField(write_only=True, required=False)
    parent_password = serializers.CharField(write_only=True, required=False)
    selected_parent = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Child
        fields = ['child_username', 'child_password', 'parent_username', 'parent_password', 'selected_parent']

    def create(self, validated_data):
        # Create the child user
        child_user = User.objects.create(
            username=validated_data['child_username'],
            password=make_password(validated_data['child_password']),
            role='child'
        )

        # Get the logged-in teacher
        teacher = self.context['request'].user

        # Handle parent creation or selection
        if validated_data.get('selected_parent'):
            parent = User.objects.get(id=validated_data['selected_parent'], role='parent')
        else:
            parent = User.objects.create(
                username=validated_data['parent_username'],
                password=make_password(validated_data['parent_password']),
                role='parent'
            )

        # Create the Child instance
        child = Child.objects.create(
            child_user=child_user,
            teacher=teacher,
            parent=parent
        )

        return child


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    """
    DRF serializer for creating a Teacher user.
    I'll force the role to 'teacher' automatically in create().
    """
    # I explicitly list the fields I want to accept from the frontend.
    # 'password' is write_only so it won't be sent back in responses.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # We set role='teacher' for all users created by this serializer.
        validated_data['role'] = 'teacher'

        # I need to hash the password before saving.
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user
