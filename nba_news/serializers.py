from rest_framework import serializers
from .models import NBANews


class NBANewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBANews
        fields = ['title', 'img_url', 'detail_url', 'paragraph', 'datetime']
