from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer

class Users(APIView) :
    def get(self, request) :
        users = User.objects.all()
        serializer = UserSerializer(instance=users, many=True)
        return Response(serializer.data)

    def post(self, request) :
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid() :
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)

class UserDetail(APIView) :
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk) :
        try :
            user = User.objects.get(pk=pk)

            if not user == request.user :
                raise PermissionDenied
            
            return user 
        except User.DoesNotExist :
            raise NotFound

    def get(self, request, pk) :
        user = self.get_object(request, pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk) :
        user = self.get_object(request, pk)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)

    def delete(self, request, pk) :
        user = self.get_object(request, pk)
        user.delete() 
        return Response(HTTP_204_NO_CONTENT)

