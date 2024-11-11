from rest_framework import serializers
from .models import rating_table
from .models import UserSubscriptions,watchlater_table,Movie,watch_history_table


class ratingSerializer(serializers.ModelSerializer):
    class Meta:
        model=rating_table
        fields=['movie','user','rating']
        
        
        

class UserSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscriptions
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},  # This will automatically use the authenticated user
        }
    
        

        
        
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'thumbnail', 'rating', 'description', 'video']  # Add all fields you want to include


        
class watchlaterSerializer(serializers.ModelSerializer):
    class Meta:
        model=watchlater_table
        fields=['user','movie','date']
        


class watchlater_get_Serializer(serializers.ModelSerializer):
    movie = MovieSerializer()  # Use the MovieSerializer to get full movie details

    class Meta:
        model = watchlater_table
        fields = ['movie', 'date']  # Include 'movie' and 'date'


class watchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=watch_history_table
        fields=['user','movie','date']
        



class watchHistory_get_Serializer(serializers.ModelSerializer):
    movie = MovieSerializer()  # Use the MovieSerializer to get full movie details

    class Meta:
        model = watch_history_table
        fields = ['movie', 'date']  # Include 'movie' and 'date'
