from rest_framework import serializers
from rent_booking_apps.listings.models import Listing, ViewHistory, SearchHistory


class ChoicesSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'id': instance[0],
            'name': instance[1]
        }


class ListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'rating',
            'number_of_reviews',
            'number_of_views'
        ]


class ViewHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ViewHistory
        exclude = ['id', 'user']

class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        exclude = ['id', 'user']


class SearchStatsSerializer(serializers.Serializer):
    term = serializers.CharField(max_length=255)
    total_searches = serializers.IntegerField()
