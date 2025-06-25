from rest_framework import serializers
from django.contrib.auth import authenticate
from base.models import User, Community, AdminAccessRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'uuid', 'username', 'email', 'role',
            'first_name', 'last_name', 'phone_number', 'profile_image'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'role',
            'first_name', 'last_name', 'phone_number'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_role(self, value):
        if value not in ['user', 'community']:
            raise serializers.ValidationError("You can only register as a 'user' or 'community' role.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user and user.is_active:
            return {
                'uuid': user.uuid,
                'email': user.email,
                'role': user.role,
                'is_admin': user.is_admin
            }
        else:
            raise serializers.ValidationError("Invalid email or password.")

class CommunitySerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    lat_lng = serializers.ReadOnlyField()

    class Meta:
        model = Community
        fields = [
            'uuid', 'name', 'email',
            'latitude', 'longitude', 'lat_lng',
            'admin', 'created', 'is_active',
        ]
        read_only_fields = ['uuid', 'lat_lng', 'created', 'admin']

class AdminAccessRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AdminAccessRequest
        fields = [
            'uuid', 'user', 'justification',
            'reviewed', 'approved', 'requested_at',
        ]
        read_only_fields = ['uuid', 'reviewed', 'approved', 'requested_at']

class AdminAccessReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccessRequest
        fields = '__all__'

