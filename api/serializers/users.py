from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.models import User, DONE
from api.utilits import is_email

class UserSerializer(serializers.ModelSerializer):
	class Meta: 
		model = User
		fields = ['username', 'email', "first_name", "last_name", 'phone']

class EmailSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True)

	def validate_email(self, email):
		if not email:
			raise serializers.ValidationError("Email cannot be empty.")

		User = get_user_model()
		try:
			user = User.objects.get(email=email)
			if not user.is_active:
				raise serializers.ValidationError("Email is not verified.")
		except User.DoesNotExist:
			pass
		return email


class CodeSerializer(serializers.Serializer):
	code = serializers.CharField(max_length=20, required=True)

	def validate_code(self, code):
		code = code.strip()
		if not code:
			raise serializers.ValidationError("Code cannot be empty.")
		if len(code) != 6: 
			raise serializers.ValidationError("Code must be 6 letters")
		if not code.isdigit():
			raise serializers.ValidationError("Code must be only numbers") 
		return code 


class SignUpSerializer(serializers.Serializer): 
	username = serializers.CharField(max_length = 200, required = True)
	phone = serializers.CharField(max_length = 13, required = True)
	first_name = serializers.CharField(max_length = 200)
	last_name = serializers.CharField(max_length = 200)
	password = serializers.CharField(max_length = 30, required = True)
	conf_password = serializers.CharField(max_length = 30, required = True)

	def validate_username(self, value:str):
		value = value.strip()
		if not value:
			raise serializers.ValidationError("Username cannot be empty")
		if len(value) < 3:
			raise serializers.ValidationError("Username must be at least 3 characters")
		if not value.replace('_', '').replace('-', '').isalnum():
			raise serializers.ValidationError("Username can only contain letters, numbers, underscores, and hyphens")
		if User.objects.filter(username=value).exists():
			raise serializers.ValidationError("Username already taken")
		return value
	
	def validate_first_name(self, value:str):
		value = value.strip()
		if not value:
			raise serializers.ValidationError("First name cannot be empty")
		if not value.isalpha():
			raise serializers.ValidationError("First name can only contain letters")
		return value

	def validate_last_name(self, value:str):
		value = value.strip()
		if not value:
			raise serializers.ValidationError("Last name cannot be empty")
		if not value.isalpha():
			raise serializers.ValidationError("Last name can only contain letters")
		return value

	def validate_phone(self, value:str):
		value = value.strip()
		if not value:
			raise serializers.ValidationError("phone cannot be empty")
		if User.objects.filter(phone=value).exists():
			raise serializers.ValidationError("Phone number is already taken")
		return value
	
	def validate(self, validated_data):
		password = validated_data.get('password')
		conf_password = validated_data.get('conf_password')

		if password != conf_password: 
			raise serializers.ValidationError("Password didn't match")
		
		return validated_data
	

class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=100, required=True)
    username = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user_input = attrs.get("user_input")

        if is_email(user_input):
            user = User.objects.filter(email=user_input, status=DONE).first()
            if not user:
                raise serializers.ValidationError("User not found")
            attrs["username"] = user.username
        else:
            attrs["username"] = user_input

        return attrs