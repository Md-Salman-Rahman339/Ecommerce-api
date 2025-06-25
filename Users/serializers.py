from rest_framework import serializers
from Users.models import MyUser

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