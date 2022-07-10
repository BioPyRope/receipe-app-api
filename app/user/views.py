''' user api views'''

from rest_framework import generics
from .serializer import UserSerializer

class CreateUserView(generics.CreateAPIView):
    serializer_class= UserSerializer