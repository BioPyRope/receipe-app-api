from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from core.models import User
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'user_name',]
        extra_kwargs={'password': {'write_only': True,"min_length":8}}
    
    def create(self, validated_data):
        return  get_user_model().objects.create_user(**validated_data)
    
    def update(self,instance,validated_data):
        '''instance: 我猜是個model get來的instance'''
        
        password=validated_data.pop("password",None)
        user=super().update(instance,validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
class TokenSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    #因為django不存在password field,用CharField來實作
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    
    def validate(self, attrs):
        
        print("attr,",attrs)
        
        email= attrs["email"]
        password=attrs["password"]
        user= authenticate(self.context.get('request'), #make sure the the request is consistant (with header)
            username=email,
            password=password,)
        
        if not user:
            raise ValidationError("user not pass auth")
        
        attrs["user"]=user
        
        return attrs
    
# class MeSerializer(serializers.Serializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'password', 'user_name',]
#         extra_kwargs={'password': {'write_only': True,"min_length":8}}
    