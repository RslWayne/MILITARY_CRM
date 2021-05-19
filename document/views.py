from django.shortcuts import render
from rest_framework import viewsets
from .models import Document
# Create your views here.
from .serializers import DocumentSerializer
from rest_framework.filters import SearchFilter
from .permissions import IsSuperUserOrReadOnly,FilterObjPermission


class DocumentModelViewSet(viewsets.ModelViewSet):
        permission_classes = [IsSuperUserOrReadOnly,FilterObjPermission]
        serializer_class = DocumentSerializer
        filter_backends = [SearchFilter]
        search_fields = ['title']

        def get_queryset(self):
            try:
                group = self.request.user.groups.all()[0].name
            except IndexError:
                docs = Document.objects.filter(document_root__in=['public'])
            if group == 'general':
                docs = Document.objects.filter(document_root__in=['public','private','secret'])
            elif group == 'president':
                docs = Document.objects.filter(document_root__in=['public', 'private', 'secret','top-secret'])
            elif group == 'serjant':
                docs = Document.objects.filter(document_root__in=['public', 'private',])

            return docs

        def perform_create(self,serializer):
            serializer.save(user=self.request.user)

