''' user api views'''


from rest_framework import generics
from .serializer import (
    UserSerializer,
    TokenSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status,authentication,permissions #class??
from core.models import User


class CreateUserView(generics.CreateAPIView):
    serializer_class= UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class=TokenSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES

class CreateUerManagerView(generics.RetrieveUpdateAPIView):#ME profile: 檢索更新view
    serializer_class= UserSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user










############legacy_CreateTokenView###############
class legacy_CreateTokenView(ObtainAuthToken):
    serializer_class=TokenSerializer
       
    def __init__(self):
        super().__init__()
        
    
    def post(self, request, *args, **kwargs):
       
        '''
        老師把以下兩個 serializer的功能丟在建立serializer class:
        
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        '''
        
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        try: #判斷帳號是否存在
            user = User.objects.get(email=request.POST['email'])
        except:
            return Response(data="User is not exist.",status=status.HTTP_400_BAD_REQUEST)
            
        
        
        if user.check_password(serializer.validated_data['password'])!=True:
            return Response(data="nodata",status=status.HTTP_400_BAD_REQUEST)
                    
        token, created = Token.objects.get_or_create(user=user)

        return Response(data={'token':token.key},status=status.HTTP_200_OK)
       
    