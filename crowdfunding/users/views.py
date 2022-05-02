from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import CustomUser
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsOwnerOrReadOnly, IsAuthorOrReadOnly
from .serializers import CustomUserSerializer, RegisterSerializer, CustomUserSerializer

# Create your views here.
class CustomUserList(APIView):

    def get(self, request):
          users = CustomUser.objects.all()
          serializer = CustomUserSerializer(users, many=True)
          return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CustomUserDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
          try:
               return CustomUser.objects.get(pk=pk)
          except CustomUser.DoesNotExist:
               raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )   

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny,]
    queryset = CustomUser.objects.all()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = token.objects.get_or_create(user=user)
     
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_owner': user.is_owner(),
        })