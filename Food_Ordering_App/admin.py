from django.contrib import admin
from .models import *
# Register your models here.

# Combine them into a single list
all_models = [UserProfile, Category, Notification, Menu, Order, Promo]

for model in all_models:
    admin.site.register(model)