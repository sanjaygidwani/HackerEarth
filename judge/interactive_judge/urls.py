from django.urls import path
from . import views
from django.views.generic import TemplateView
from interactive_judge.views import HomeView

urlpatterns = [
	path('',HomeView.as_view(),name='home'),
	path('add_problems/', views.new_problem, name='add_problem'),
	path('practice/', views.practice,name='practice'),
	path('problem/<int:pk>',views.problem_load,name='problem_load'),
	path('submit/<int:pk>',views.problem_submit,name='submit'),
]
