from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from .filters import ClientFilter
from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """Handle creating and listing clients"""
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    filterset_class = ClientFilter
    permission_classes = (permissions.IsAuthenticated,)
