# disease_predictor_project/predictor/views.py

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Symptom
from .serializers import SymptomSerializer
from .ml_model import model_utils # Import our ML utility functions

def home_view(request):
    """
    Renders the main prediction page.
    """
    return render(request, 'predictor/index.html')

class SymptomListView(generics.ListAPIView):
    """
    API endpoint to list all available symptoms.
    """
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer

class PredictionView(APIView):
    """
    API endpoint to receive symptoms and return a disease prediction.
    """
    def post(self, request, *args, **kwargs):
        selected_symptom_names = request.data.get('symptoms', [])

        if not selected_symptom_names:
            return Response(
                {"error": "No symptoms provided. Please select at least one symptom."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure symptoms are strings and in a list
        if not isinstance(selected_symptom_names, list) or not all(isinstance(s, str) for s in selected_symptom_names):
             return Response(
                {"error": "Symptoms must be a list of strings."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the ML model utility function
        try:
            # In a real app, you might validate symptom names against your Symptom model
            # and sanitize input before passing to ML.
            prediction_result = model_utils.predict_disease(selected_symptom_names)

            return Response(prediction_result, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error for debugging
            print(f"Error during prediction: {e}")
            return Response(
                {"error": "An internal error occurred during prediction.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )