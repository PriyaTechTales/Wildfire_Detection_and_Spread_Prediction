from django.shortcuts import render, redirect
from django.http import JsonResponse
from .ml_model import predict_fire
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
import pickle
import numpy as np
import json
import joblib


def home(request):
    return render(request, 'home.html')  # Show home page to all users

def about(request):
    return render(request, 'about.html')  # ✅ Loads about.html

def contact(request):
    return render(request, 'contact.html')

def main(request):
    return render(request, 'main.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('wildfire_detection')  # Redirect to prediction page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def logout_view(request):
    logout(request)  # Logs out the user
    messages.success(request, 'Account Logout successfully!.')
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_path = f"media/{image.name}"
        
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        result = predict_fire(image_path)
        os.remove(image_path)  # Clean up after prediction

        return JsonResponse({'prediction': result})

    return render(request, 'upload.html')

def wildfire_detection(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image = request.FILES['image']
            
            # Create media directory if it doesn't exist
            media_dir = os.path.join('media', 'temp')
            os.makedirs(media_dir, exist_ok=True)
            
            # Save the uploaded image
            image_path = os.path.join(media_dir, image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            print(f"Processing image: {image_path}")
            
            # Get prediction from YOLOv8 model
            result = predict_fire(image_path)
            
            print(f"Model result: {result}")
            
            # Clean up the temporary file
            if os.path.exists(image_path):
                os.remove(image_path)
            
            return JsonResponse(result)
            
        except Exception as e:
            print(f"Error in wildfire_detection: {str(e)}")
            return JsonResponse({
                'status': 'Error', 
                'error': str(e)
            })
    elif request.method == 'POST':
        return JsonResponse({
            'status': 'Error',
            'error': 'No image file provided'
        })

    return render(request, 'detection.html')

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def update_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        try:
            # Delete old avatar if it exists
            if request.user.profile.avatar:
                request.user.profile.avatar.delete()
            
            request.user.profile.avatar = request.FILES['avatar']
            request.user.profile.save()
            return JsonResponse({'success': True, 'url': request.user.profile.avatar.url})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'No file provided'})

def load_spread_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'forest_fire_model.pkl')
    scaler_path = os.path.join(base_dir, 'forest_fire_scaler.pkl')
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        return model, scaler
    except Exception as e:
        print(f"Error loading spread model: {str(e)}")
        return None, None

def predict_spread(request):
    if request.method == 'POST':
        try:
            # Try to get data from both JSON and form-data formats
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            # Extract features and convert to float
            features = np.array([[
                float(data.get('ffmc', 0)),
                float(data.get('dmc', 0)),
                float(data.get('dc', 0)),
                float(data.get('isi', 0)),
                float(data.get('temp', 0)),
                float(data.get('rh', 0)),
                float(data.get('wind', 0)),
                float(data.get('rain', 0))
            ]])
            
            # Load the model and scaler
            with open('forest_fire_model.pkl', 'rb') as f:
                saved_data = pickle.load(f)
                model = saved_data['model']
                scaler = saved_data['scaler']
            
            # Scale the features
            features_scaled = scaler.transform(features)
            
            # Make prediction
            prediction = model.predict(features_scaled)[0]
            
            return JsonResponse({'area': float(prediction)})
            
        except Exception as e:
            print(f"Prediction error: {str(e)}")  # Add logging for debugging
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
