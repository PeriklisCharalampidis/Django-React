from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Model
from typing import Any
from django.db.models.manager import BaseManager

class CreateUserView(generics.CreateAPIView):
    queryset = User._default_manager.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> Any:
        # Only return notes created by the current user
        return Note._default_manager.filter(author=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the author as the current user
        serializer.save(author=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        note = self.get_object()
        # Only allow deletion if the user is the author
        if note.author != request.user:
            return Response(
                {"detail": "You do not have permission to delete this note."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)