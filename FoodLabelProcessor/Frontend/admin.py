from django.contrib import admin
from .models import Serving
from .models import NutritionUser
from .models import DateEaten

admin.site.register(Serving)
admin.site.register(DateEaten)
admin.site.register(NutritionUser)
