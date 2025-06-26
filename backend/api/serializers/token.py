from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from base.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD  # Use email as the username field

    def validate(self, attrs):
        # Accept 'email' from the request and map it to 'username' for authentication
        if 'email' in attrs:
            attrs['username'] = attrs['email']
        return super().validate(attrs)
