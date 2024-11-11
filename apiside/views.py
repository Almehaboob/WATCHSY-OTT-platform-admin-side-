from rest_framework import permissions,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.authtoken.models import Token
from .models import User_table,Movie,Plan,UserSubscriptions,watchlater_table,watch_history_table
from .serializers import ratingSerializer,UserSubscriptionsSerializer,watchlaterSerializer,watchlater_get_Serializer,watchHistorySerializer,watchHistory_get_Serializer
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not email or not password:
        return Response({'error': 'All fields are required'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": 'Username already exists'}, status=400)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)
    
    user = User(
        username=username,
        email=email,
        password=make_password(password)
    )
    user.save()
    
    # Generate Token for the user
    # token, created = Token.objects.get_or_create(user=user)
    
    return Response({'message': 'Account created successfully'}, status=201)





@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password'}, status=401)

    # Check if the user is blocked
    if user.is_blocked:
        return Response({'error': 'Your account is blocked. Please contact support.'}, status=403)

    # Check password
    if check_password(password, user.password):
        # Generate Token for the user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': user.id  # Include user ID in the response
        }, status=200)
    else:
        return Response({'error': 'Invalid email or password'}, status=401)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def change_password(request):
    user = request.user  # Get the currently authenticated user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    # Check if both old and new passwords are provided
    if not old_password or not new_password:
        return Response({'error': 'Old password and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify the old password
    if not check_password(old_password, user.password):
        return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the new password is different from the old one
    if old_password == new_password:
        return Response({'error': 'New password cannot be the same as the old password'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the password and save the user
    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)




@api_view(['DELETE'])  # Use DELETE method
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def logout(request):
    try:
        # Get the user's token and delete it
        request.user.auth_token.delete()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token or user not logged in"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def movie_list(request):
    movies = Movie.objects.all()
    data = [{
        'id': movie.id,               # Include the movie ID
        'title': movie.title,
        'thumbnail': movie.thumbnail,  # Thumbnail field is included
        'rating': movie.rating,
    } for movie in movies]
    return Response(data)

# 

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def movie_details(request, id):
    try:
        movie = Movie.objects.get(pk=id)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'title': movie.title,
        'thumbnail': movie.thumbnail, # Uncomment if you have a thumbnail field
        'video': movie.video,  # Uncomment if you have a video field
        'description': movie.description,
        'rating': movie.rating,
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plan_list(request):
    plans = Plan.objects.all()
    data = [{
        'id':plan.id,
        'name': plan.name,  
        'thumbnail': plan.thumbnail, 
        'price': plan.price , 
        'duration':plan.duration
    } for plan in plans]
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plan_details(request,id):
    try:
        plan = Plan.objects.get(pk=id)
    except Plan.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=404)
        
    data={
        'title':plan.name,
        'thumbnail':plan.thumbnail,
        'duration':plan.duration,
        'price':plan.price
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription(request):
    if request.method == 'POST':
        serializer = UserSubscriptionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_history(request, user_id):
    try:
        subscriptions = UserSubscriptions.objects.filter(user__id=user_id)
        if not subscriptions.exists():
            return Response({'error': 'No subscriptions found for this user'}, status=404)


        serializer = UserSubscriptionsSerializer(subscriptions, many=True)
        return Response(serializer.data, status=200)
        
    except User_table.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_rating(request):
        serializer = ratingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"rating added successfully"} )
        else:
            return Response(serializer.errors)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watchlater_list(request):
    if request.method == 'POST':
        serializer = watchlaterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Movie added to your Watch Later list"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        user = request.user  # Get the authenticated user
        watchlater_movies = watchlater_table.objects.filter(user=user)  # Filter movies for the user
        serializer = watchlaterSerializer(watchlater_movies, many=True)  # Serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watch_later(request, user_id):
    try:
        watch_later_items = watchlater_table.objects.filter(user=user_id)
        serializer = watchlater_get_Serializer(watch_later_items, many=True)
        
        return Response(serializer.data, status=200)
    
    except watchlater_table.DoesNotExist:
        return Response({"message": "No watch later items found."}, status=404)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_watch_later(request, movie_id):
    try:
        # Filter by the movie ID and the currently authenticated user
        user = request.user
        watchlater_entries = watchlater_table.objects.filter(movie__id=movie_id, user=user)
        
        if watchlater_entries.exists():
            watchlater_entries.delete()
            return Response({"message": "Movie(s) deleted from your Watch Later list."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Movie not found in your Watch Later list."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def watchHistory_list(request):
    if request.method == 'POST':
        # Include the authenticated user in the request data
        data = request.data.copy()  # Create a copy of the request data
        data['user'] = request.user.id  # Set the user field to the authenticated user's ID

        serializer = watchHistorySerializer(data=data)  # Use the serializer
        if serializer.is_valid():
            serializer.save()  # Save the new entry to the database
            return Response({'message': 'Watch history added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watch_history(request, user_id):
    try:
        watch_later_items = watch_history_table.objects.filter(user=user_id)
        serializer = watchHistory_get_Serializer(watch_later_items, many=True)
        
        return Response(serializer.data, status=200)
    
    except watch_history_table.DoesNotExist:
        return Response({"message": "No watch history items found."}, status=404)
