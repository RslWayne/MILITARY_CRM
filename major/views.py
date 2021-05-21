from _testcapi import raise_exception

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView


from .models import Dossier
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *

# Create your views here.
from document.serializers import RegisterSerializer


class DossierModelViewSet(APIView):

    def get(self,request,*args,**kwargs):
        try:
            dossier = Dossier.objects.get(user=request.user)
        except Dossier.DoesNotExist:
            return Response({"data":"Dossier doesnt exist"},status=status.HTTP_404_NOT_FOUND)
        serializer = DossierSerializer(dossier)
        return Response(serializer.data)

    def put(self,request,*args,**kwargs):
        dossier = Dossier.objects.get(user=request.user)
        serializer = DossierSerializer(dossier,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self,request,*args,**kwargs):
        dossier = Dossier.objects.get(user=request.user)
        dossier.delete()
        return Response({"data":"Delete successful!"})



class RegisterViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = RegisterSerializer

class AuthView(ObtainAuthToken):

        def post(self,request,*args,**kwargs):
            serializers = self.serializer_class(data=request.data,
                                                context={'request':request})
            serializers.is_valid(raise_exception=True)
            user = serializers.validated_data['user']
            token,created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key})

