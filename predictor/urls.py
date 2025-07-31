

from django.urls import path
from . import views

app_name = 'predictor' # Namespace for this app's URLs

urlpatterns = [
    path('', views.home_view, name='home'), # Our main prediction page

    # API Endpoints
    path('api/symptoms/', views.SymptomListView.as_view(), name='symptom_list'),
    path('api/predict/', views.PredictionView.as_view(), name='predict_disease'),
]