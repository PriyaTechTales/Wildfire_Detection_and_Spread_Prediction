from django.urls import path
from wildfire_app import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home, name='home'),
    path("about.html", views.about, name='about'),        # ✅ Now allows .html
    path("contact.html", views.contact, name='contact'),
    path("main.html", views.main, name='main'),
    path("login.html", views.login_view, name="login"),
    path("signup.html", views.signup, name="signup"),
    path("detect/", views.wildfire_detection, name='wildfire_detection'),
    path("upload/", views.upload_image, name='upload_image'),
    path("profile/", views.profile, name='profile'),
    path("edit-profile/", views.edit_profile, name='edit_profile'),
    path("update-avatar/", views.update_avatar, name='update_avatar'),
    path("logout/", LogoutView.as_view(next_page='home'), name='logout'),
    path('predict_spread/', views.predict_spread, name='predict_spread'),
]
