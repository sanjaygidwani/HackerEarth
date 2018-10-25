from django.urls import path
from . import views
from django.views.generic import TemplateView
from interactive_judge.views import HomeView

urlpatterns = [
	path('',HomeView.as_view()),
	path('add_problems/', TemplateView.as_view(template_name='add_problems.html')),
    path('problems/', TemplateView.as_view(template_name='problems.html')),
]
