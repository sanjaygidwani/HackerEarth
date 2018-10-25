from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Problems

# Create your views here.

# class based views
class HomeView(TemplateView):

	template_name = 'home.html'

	def get_context_data(self, *args, **kwargs):
		context = super(HomeView, self).get_context_data(*args, **kwargs)
		context = {
			"html_var": True
		}
		return context

'''def problem_new(request):

	#create new problem

def problem_edit(request,pk):

	#editing existing problem

def problem_submit(request):

	#handling submission request on a problem
'''
	
def practice(request):

	#display all problems
	problems = Problems.objects.all()

	
#'''

