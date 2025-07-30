# disease_predictor_project/predictor/admin.py

from django.contrib import admin
from .models import Symptom

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('name',) # Display 'name' in the list view
    search_fields = ('name',) # Allow searching by 'name'