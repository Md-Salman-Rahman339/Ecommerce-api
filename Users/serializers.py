from rest_framework import serializers
from Users.models import MyUser
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')  
        user = MyUser.objects.create_user(password=password, **validated_data)
        return user

class UserLoginSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=MyUser
        fields=['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
      password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
      password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

      class Meta:
          fields=['password','password2']

      def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password !=password2:
            raise serializers.ValidationError("Password and confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs  


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email=attrs.get('email')
        if MyUser.objects.filter(email=email).exists():
            user=MyUser.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link=uid+'/'+token
            body='Click Following Link to Reset your password '+link
            data={
                'subject':'Reset your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')  


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
           password=attrs.get('password')
           password2=attrs.get('password2')
           uid=self.context.get('uid')
           token=self.context.get('token')
           if password !=password2:
               raise serializers.ValidationError("Password and Confirm Password doesn't match")
           id=smart_str(urlsafe_base64_decode(uid))
           user=MyUser.objects.get(id=id)
           if not PasswordResetTokenGenerator().check_token(user,token):
               raise serializers.ValidationError('Token is not Valid or Expired')
           user.set_password(password)
           user.save()
           return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is not valid or Expired')    