from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Problems,TestCase

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
	
'''

def problem_submit(request,pk):
	problem = get_object_or_404(Problems,pk=pk)
	print(problem)
	testcases = TestCase.objects.filter(pid=problem.id)
	type=problem.type
	for i in testcases:
		#function call to get verdict and all other values from system
		function_call(type,i.testfile_user,i.testfile_interactor)

	#calling template for submission page
	return render(request,'problem_submit.html',context)

	#handling submission request on a problem

	
def practice(request):

	#display all problems
	problems = Problems.objects.all()
	return render(request,'problem_list.html',{'problems':problems})


	
#'''

