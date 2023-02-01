from django.urls import path
from chatapp import views
from django.conf import settings
 
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("reset-update", views.reset_password, name="reset-update"),
    path("chat/<int:id>", views.chat, name="chat"),
    path("chat-create/<int:id>", views.create_chat, name="chat-create"),
    path("users", views.users, name="users"),
    path('profile',views.profile,name='profile'),
    path('profile-update',views.profile_update,name='profile-update')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
