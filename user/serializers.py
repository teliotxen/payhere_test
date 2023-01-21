from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from . models import User


class JWTSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        write_only=True,
        max_length=20
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta(object):
        model = User
        fields = ['email', 'password']

    def save(self, request):
        user = super().save()
        user.email = self.validated_data['email']
        user.set_password(self.validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        email = data.get('email', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("user already exists")
        return data


class JWTLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        write_only=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta(object):
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("user account not exist")

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'refresh': refresh,
            'access': access,
        }
        return data

