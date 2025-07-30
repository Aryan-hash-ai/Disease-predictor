# disease_predictor_project/predictor/serializers.py

from rest_framework import serializers
from .models import Symptom

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['id', 'name'] # We only need id and name for the frontend list