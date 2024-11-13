import django_filters
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter

from events.models import Event
from events.serializers import EventSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить GET, HEAD или OPTIONS запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить изменения только если пользователь является организатором
        return obj.organizer == request.user

class EventFilter(django_filters.FilterSet):
    # Фильтрация по полям: создание события, назначение события
    time_created__gte = django_filters.DateTimeFilter(field_name='time_created', lookup_expr='gte', label='Time Created After')
    time_created__lte = django_filters.DateTimeFilter(field_name='time_created', lookup_expr='lte', label='Time Created Before')
    date__gte = django_filters.DateTimeFilter(field_name='date', lookup_expr='gte', label='Event Date After')
    date__lte = django_filters.DateTimeFilter(field_name='date', lookup_expr='lte', label='Event Date Before')

    # Поиск по полям: ID организатора, ID приглашенных пользователей, локации, заголовку
    organizer_id = django_filters.NumberFilter(field_name='organizer', lookup_expr='exact', label='Organizer ID')
    invited_user_id = django_filters.NumberFilter(field_name='invited_users', lookup_expr='exact', label='Invited User ID')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains', label='Location')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')

    class Meta:
        model = Event
        fields = []


class EventsAPIViews(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = EventFilter
    search_fields = ['title']  # Позволяет искать по названию


    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Сортировка по дате события
        ordering = self.request.query_params.get('ordering', 'time_created')  # Сортировка по умолчанию по дате
        return queryset.order_by(ordering)


class EventDetailAPIViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]



def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('login')
