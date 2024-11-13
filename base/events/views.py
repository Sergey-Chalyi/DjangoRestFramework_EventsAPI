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
    """
    Custom permission class to allow read access to all users, but only allow to
    write access to the owner of an object.

    This permission is used to ensure that only the organizer of an event can
    modify or delete it, while allowing all authenticated users to view events.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determine if the user has permission to perform the requested action on the object.

        Parameters:
        request (HttpRequest): The request being made.
        view (View): The view handling the request.
        obj (Model): The object being accessed.

        Returns:
        bool: True if the user has permission, False otherwise.
        """
        # allow GET, HEAD or OPTIONS requests to everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # allow changes only if user is organizer
        return obj.organizer == request.user


class EventFilter(django_filters.FilterSet):
    """
    A Django FilterSet for filtering and searching Event objects.

    This class allows users to filter events based on various criteria such as event creation and assignment dates,
    organizer and invited user IDs, location, and title. It also provides search functionality for the title field.
    """

    # Filter events based on the time they were created.
    # 'gte' and 'lte' represent 'greater than or equal to' and 'less than or equal to' respectively.
    time_created__gte = django_filters.DateTimeFilter(field_name='time_created', lookup_expr='gte', label='Time Created After')
    time_created__lte = django_filters.DateTimeFilter(field_name='time_created', lookup_expr='lte', label='Time Created Before')

    # Filter events based on the event date.
    date__gte = django_filters.DateTimeFilter(field_name='date', lookup_expr='gte', label='Event Date After')
    date__lte = django_filters.DateTimeFilter(field_name='date', lookup_expr='lte', label='Event Date Before')

    # Filter events based on the organizer's ID.
    organizer_id = django_filters.NumberFilter(field_name='organizer', lookup_expr='exact', label='Organizer ID')

    # Filter events based on the invited user's ID.
    invited_user_id = django_filters.NumberFilter(field_name='invited_users', lookup_expr='exact', label='Invited User ID')

    # Filter events based on the location.
    # 'icontains' represents 'case-insensitive contains'.
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains', label='Location')

    # Filter events based on the title.
    # 'icontains' represents 'case-insensitive contains'.
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')

    class Meta:
        model = Event
        fields = []


class EventsAPIViews(generics.ListCreateAPIView):
    """
    A view for listing and creating Event objects.

    This view inherits from Django REST Framework's ListCreateAPIView, which provides
    functionality for listing a queryset and creating new objects. It uses the Event model,
    EventSerializer serializer class, and applies authentication and permission checks.

    The view also supports filtering, searching, and sorting of Event objects based on various criteria.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = EventFilter
    search_fields = ['title']


    def perform_create(self, serializer):
        """
        Perform additional actions before creating a new Event object.

        This method is called after the serializer has validated the data and before the object is saved.
        In this case, it sets the 'organizer' field of the Event object to the current user.

        Parameters:
        serializer (EventSerializer): The serializer instance used to create the new Event object.
        """
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        """
        Modify the queryset before returning it.

        This method is called before returning the queryset. In this case, it adds sorting functionality
        based on the 'ordering' query parameter.

        Returns:
        QuerySet: The modified queryset.
        """
        queryset = super().get_queryset()

        # sorting
        ordering = self.request.query_params.get('ordering', 'time_created')  # time_created default
        return queryset.order_by(ordering)


class EventDetailAPIViews(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting individual Event objects.

    This view inherits from Django REST Framework's RetrieveUpdateDestroyAPIView, which provides
    functionality for retrieving, updating, and deleting a single object. It uses the Event model,
    EventSerializer serializer class, and applies authentication and permission checks.

    Attributes:
    queryset (QuerySet): The queryset of Event objects to be used for this view.
    serializer_class (EventSerializer): The serializer class used to serialize and deserialize Event objects.
    permission_classes (list): A list of permission classes that determine access to this view.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]



def login(request):
    """
    A view that renders the login page.

    This view simply renders the login.html template. It is used for logging in users via
    Google OAuth2.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered login page.
    """

    return render(request, 'login.html')


@login_required
def home(request):
    """
    A view that renders the home page for logged in users.

    This view renders the home.html template and is only accessible to users who are logged in.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered home page.
    """

    return render(request, 'home.html')


def logout_view(request):
    """
    A view that logs out the current user and redirects them back to the login page.

    This view is used to log out users and redirect them to the login page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: A redirect to the login page.
    """

    logout(request)
    return redirect('login')
