from datetime import timedelta
from django.db.models import Count
from rest_framework import generics, viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rent_booking_apps.bookings.models import Booking, BookingStatus
from rent_booking_apps.listings.filters import CustomSearchFilter
from rent_booking_apps.listings.models import PropertyType, Listing, ViewHistory, SearchHistory
from rent_booking_apps.listings.serializers import ChoicesSerializer, ViewHistorySerializer, SearchHistorySerializer, \
    SearchStatsSerializer, ListingSerializer
from rent_booking_apps.reviews.serializers import ReviewSerializer
from rent_booking_apps.users.permissions import IsOwnerOrReadOnly


class PropertyTypeListView(generics.ListAPIView):
    queryset = PropertyType.choices
    serializer_class = ChoicesSerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['results_label'] = 'results'
        return context

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {
            self.get_serializer_context()['results_label']: response.data
        }
        return response


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        CustomSearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = {
        'price': ['lte', 'gte'],    # Цена (возможность указать минимальную и максимальную цену)
        'rooms': ['range'],     # Количество комнат (возможность указать диапазон количества комнат)
        'property_type': ['exact'],     # Тип жилья (возможность выбрать тип жилья квартира,
                                        # дом, студия и т.д.)
        'address': ['icontains'],   # Местоположение: (возможность указать город или район в Германии)
        'parking': ['exact'],
        'room_service': ['exact'],
        'all_time_reception': ['exact'],
        'wifi_included': ['exact'],
        'wheelchair_accessible': ['exact'],
        'pool': ['exact'],
        'non_smoking_rooms': ['exact'],
        'airport_shuttle': ['exact'],
    }
    # Пользователь вводит ключевые слова, по которым производится поиск
    # в заголовках и описаниях объявлений
    search_fields = ['title', 'description']
    # Возможность сортировки по цене (возрастание/убывание),
    # дате добавления (новые/старые)
    ordering_fields = [
        'price',
        'created_at',
        'rating',
        'number_of_reviews',
        'number_of_views'
    ]
    ordering = ['id']

    def get_queryset(self):     # "Получить список всех активных объявлений",
        if self.action == 'list':
            return Listing.objects.filter(is_active=True)
        return Listing.objects.all()

    def get_permissions(self):      #   "Создать новое объявление"
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):   # "Обновить объявление, Частично обновить объявление"
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):   #"Получить детальную информацию об объявления, Удалить объявление"
        instance = self.get_object()
        # Запрет на просмотр неактивных объявлений, если это не владелец
        if not instance.is_active and instance.owner != request.user:
            raise PermissionDenied()
        # Если это не владелец, записываем просмотр
        if request.user.is_authenticated and instance.owner != request.user:
            ViewHistory.objects.update_or_create(
                listing=instance,
                user=request.user
            )
            instance.update_views()
        return super().retrieve(request, *args, **kwargs)

    def my_created(self, request): #"Получить список объявлений созданных аутентифиц-м пользователем"
        queryset = Listing.objects.filter(owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def my_view_history(self, request):     #"Получить историю просмотренных объявл. аутентифиц-го пользователя"
        view_history = ViewHistory.objects.filter(
            user=request.user
        ).order_by('-viewed_at')
        view_history = [view for view in view_history]
        serializer = ViewHistorySerializer(
            view_history, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def my_search_history(self, request):   #"Получить историю поисковых запросов аутентифицированного пользователя")
        search_history = SearchHistory.objects.filter(
            user=request.user
        ).order_by('-searched_at')
        search_history = [search for search in search_history]
        serializer = SearchHistorySerializer(search_history, many=True)
        return Response(serializer.data)

    def search_stats(self, request):        #"Получить список популярных поисковых запросов"
        search_stats = (SearchHistory.objects.values('term')
                        .annotate(total_searches=Count('term')).order_by('-total_searches'))
        search_stats = [search for search in search_stats]
        serializer = SearchStatsSerializer(search_stats, many=True)
        return Response(serializer.data)

    def reserved_periods(self, request, pk=None):   #"Получить список забронированых
        listing = self.get_object()                             #периодов для объявления")
        bookings = Booking.objects.filter(
            listing=listing,
            status=BookingStatus.CONFIRMED
        ).values('check_in_date', 'check_out_date')
        reserved_dates = [
            {
                'check_in': booking['check_in_date'],
                'check_out': booking['check_out_date']
            }
            for booking in bookings
        ]
        return Response(reserved_dates)

    def reserved_dates(self, request, pk=None): # "Получить список забронированых дат для объявления")
        listing = self.get_object()
        bookings = Booking.objects.filter(
            listing=listing,
            status=BookingStatus.CONFIRMED
        ).values('check_in_date', 'check_out_date')
        reserved_dates = set()
        for booking in bookings:
            check_in_date = booking['check_in_date']
            check_out_date = booking['check_out_date']
            current_date = check_in_date
            while current_date <= check_out_date:
                reserved_dates.add(current_date)
                current_date += timedelta(days=1)
        reserved_dates = sorted(list(reserved_dates))
        return Response(reserved_dates)

    def reviews(self, request, pk=None):    # "Получить список отзывов для объявления")
        listing = self.get_object()
        reviews = listing.reviews.all()
        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def property_types(self, request):  #"Получить виды недвижимости с их кодами"
        queryset = PropertyType.choices
        serializer = ChoicesSerializer(queryset, many=True)
        return Response({'results': serializer.data})
