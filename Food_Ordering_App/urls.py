from django.urls import path
from . import views
from django.conf.urls import handler400, handler403, handler404, handler500


handler400 = views.custom_400_view
handler403 = views.custom_403_view
handler404 = views.custom_404_view
handler500 = views.custom_500_view
# handler503 = views.custom_503_view

urlpatterns = [
    #### HOME PAGES ######
    #### HOME PAGES ######
    #### HOME PAGES ######
    path('', views.Home, name='home'),
    path('index/', views.Home2, name='home2'),
    
    #### AUTHENTICATION ######
    #### AUTHENTICATION ######
    #### AUTHENTICATION ######
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('afterlogin_view/', views.afterlogin_view, name='afterlogin_view'),
    path('auth-signup/', views.RegisterView.as_view(), name='user_register'),
    path('accounts/login/', views.SignInView.as_view(), name='user_login'),
    path('auth-signout/', views.SignOutView, name='user_logout'),

    #### DRIVER PAGES  ######
    path('driver_home/', views.driver_home, name='driver_home'),
    path('driver_order/', views.driver_order, name='driver_order'),


    #### OTHER PAGES ######
    #### OTHER PAGES ######
    #### OTHER PAGES ######
    path('menu/', views.menu, name='menu'),
    path('add_category/', views.add_category, name='add_category'),
    path('settings/', views.settings, name='settings'),
    path('food_order/', views.food_order, name='food_order'),
    path('user_update_profile/', views.UserProfileUpdateForm, name='profile_update'),
    path('order_history/', views.order_history, name='order_history'),
    path('bill/', views.bill, name='bill'),
    path('page404/', views.page404, name='page404'),
]

from django.conf import settings
from django.conf.urls.static import static
# Add static and media URL patterns in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    