from rest_framework import serializers
from .models import CustomUser, EmailConfirmation


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def validate_email(self, value):
        if not(self._validate_st_mail(value)):
            raise serializers.ValidationError('incorrect email')
        return value

    @staticmethod
    def check_user(data):
        email = data.get('email')
        existing_user = CustomUser.objects.filter(email=email).first()
        if not(email and existing_user):
            return
        if existing_user.is_active:
            raise serializers.ValidationError('such an email already exists')
        existing_user.delete()

    @staticmethod
    def _validate_st_mail(email):
        if email.startswith('st') and email.endswith('@student.spbu.ru'):
            return True
        return False

class EmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        if not EmailConfirmation.objects.filter(email=email).exists():
            raise serializers.ValidationError('there is no user with this email address')

        if CustomUser.objects.get(email=email).is_active:
            raise serializers.ValidationError('the email has already been confirmed')

        email_confirmation: EmailConfirmation = EmailConfirmation.objects.get(email=email)
        if email_confirmation.is_code_expired():
            CustomUser.objects.get(email=email).delete()
            raise serializers.ValidationError('the email confirmation time has expired')

        if email_confirmation.code != code:
            raise serializers.ValidationError('invalid confirmation code')

        return data

    @staticmethod
    def get_user(email):
        user = CustomUser.objects.filter(email=email).first()
        if user:
            return user






