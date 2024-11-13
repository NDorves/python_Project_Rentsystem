from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class PropertyType(models.IntegerChoices):
    APARTMENT = 0, _('Apartment')
    HOUSE = 1, _('House')
    STUDIO = 2, _('Studio')


class Listing(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='poster_images/',
                              help_text='Upload image', null=True, blank=True)  # Загрузите изображение
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, help_text="Landmark (location)")
    site_link = models.URLField(max_length=150, help_text="Object page link (https://www.google.de/maps/",
                                verbose_name="Link to page", null=True)
    property_type = models.IntegerField(choices=PropertyType.choices, default=PropertyType.APARTMENT)
    rooms = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0.0)
    number_of_reviews = models.IntegerField(default=0)
    number_of_views = models.IntegerField(default=0)
    parking = models.BooleanField(default=False, null=True)
    pets_allowed = models.BooleanField(default=False, null=True)
    room_service = models.BooleanField(default=False, null=True)
    all_time_reception = models.BooleanField(default=False, null=True)
    wifi_included = models.BooleanField(default=False, null=True)
    wheelchair_accessible = models.BooleanField(default=False, null=True)
    pool = models.BooleanField(default=False, null=True)
    non_smoking_rooms = models.BooleanField(default=False, null=True)
    airport_shuttle = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']

    def update_views(self):
        '''
        Обновление счетчика просмотров объявления
        '''
        self.number_of_views = self.view_history.count()
        self.save()

    def update_rating(self):
        '''
        Обновление рейтинга и счетчика отзывов

        '''
        reviews = self.reviews.aggregate(
            rating=models.Avg('rating'),
            number_of_reviews=models.Count('id')
        )
        self.rating = reviews['rating'] or 0.0
        self.number_of_reviews = reviews['number_of_reviews']
        self.save()


class ViewHistory(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='view_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='view_history')
    viewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} viewed {self.listing}'

    class Meta:
        ordering = ['-viewed_at']


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history',)
    term = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} searched {self.term}'

    class Meta:
        ordering = ['-searched_at']
