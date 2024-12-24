from rest_framework import serializers

from .models import CustomUser, EmailConfirmation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    @staticmethod
    def check_user(data):
        email = data.get("email")
        existing_user = CustomUser.objects.filter(email=email).first()
        if not (email and existing_user):
            return
        if existing_user.is_active:
            raise serializers.ValidationError("Пользователь с такой почтой уже зарегестрирован")
        existing_user.delete()


class EmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        code = data.get("code")

        if not EmailConfirmation.objects.filter(email=email).exists():
            raise serializers.ValidationError("Не существует пользователя с таким именем")

        if CustomUser.objects.get(email=email).is_active:
            raise serializers.ValidationError("Эта почта уже подтверждена")

        email_confirmation: EmailConfirmation = EmailConfirmation.objects.get(email=email)
        if email_confirmation.is_code_expired():
            CustomUser.objects.get(email=email).delete()
            raise serializers.ValidationError("Истекло время действия кода, зарегистрируйтесь заново")

        if email_confirmation.code != code:
            raise serializers.ValidationError("Неверный код")

        return data

    @staticmethod
    def get_user(email):
        user = CustomUser.objects.filter(email=email).first()
        if user:
            return user

