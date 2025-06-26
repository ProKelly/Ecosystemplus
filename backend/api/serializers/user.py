from rest_framework import serializers
from django.contrib.auth import authenticate
from base.models import User, Community, AdminAccessRequest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'uuid','email', 'role',
            'first_name', 'last_name', 'phone_number', 'profile_image'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'role',
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
        # Set username to email automatically
        email = validated_data.get('email')
        user = User(username=email, **validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD  # Use email as the username field

    def validate(self, attrs):
        print(f"CustomTokenObtainPairSerializer.validate called with attrs: {attrs}")
        if 'email' in attrs:
            attrs['username'] = attrs['email']
        print(f"Authenticating with username: {attrs.get('username')}, password: {'*' * len(attrs.get('password', ''))}")
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
        print(f"authenticate() returned: {user}")
        if user is None:
            raise serializers.ValidationError("No active account found with the given credentials")
        # Generate token for the authenticated user directly
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        # Optionally add user info
        data['user'] = {
            'uuid': str(user.uuid),
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        print(f"Returning token data: {data}")
        return data

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Debug print for login attempts
        print(f"Login attempt: email={email}, password={'*' * len(password) if password else None}")

        try:
            user_obj = User.objects.get(email=email)
            print(f"User found: username={user_obj.username}, is_active={user_obj.is_active}")
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            print("User with this email does not exist.")
            user = None

        if user and user.is_active:
            return {
                'uuid': user.uuid,
                'email': user.email,
                'role': user.role,
                'is_admin': user.is_admin
            }
        else:
            print("Invalid email or password.")
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

