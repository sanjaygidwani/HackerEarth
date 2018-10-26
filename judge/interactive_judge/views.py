from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Problems,TestCase,Submissions,ProblemSubmission
from .interactive import execute_interactive_testcase
from django.http import JsonResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess

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

	#editing existing problem`
	
'''

def problem_load(request,pk):

	problem = get_object_or_404(Problems, pk=pk)
	return render(request,'problem_load.html',{'problem':problem})

def problem_submit(request,pk):

	problem = get_object_or_404(Problems, pk=pk)
	sub = Submissions()
	sub.username = request.user
	sub.pid = problem.id
	sub.save()
	user_solution = request.FILES['user_solution']
	testcases = TestCase.objects.filter(pid=problem.id)
	type = problem.type
	prob_sub = ProblemSubmission()
	json_response = {}
	ind=0
	for i in testcases:
		# function call to get verdict and all other values from system
		cxt = {
			'id': problem.id, 'type': type, 'userinputfile':i.testfile_user, 'interactorinputfile':i.testfile_interactor,'usercode':user_solution,
		}
		obj = execute_interactive_testcase(cxt)
		prob_sub.pid = problem.id
		prob_sub.sid = sub.id
		prob_sub.memory = obj['memory']
		prob_sub.time = obj['time']
		prob_sub.verdict = obj['verdict']
		prob_sub.testid = i.id
		prob_sub.save()
		json_response['ind':obj]
		ind+=1

	return JsonResponse(json_response)





def practice(request):

    # display all problems
    problems = Problems.objects.all()
    return render(request, 'problem_list.html', {'problems': problems})


# '''

def new_problem(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        prob_details = Problems()
        prob_details.prob_title = request.POST['name']
        prob_details.prob_description = request.POST['problem_statement']
        prob_details.sample_exp = request.POST['explanation']
        prob_details.time_limit = request.POST['time_limit']
        prob_details.input_type = request.POST['input_type']
        prob_details.memory_limit = request.POST['memory_limit']
        prob_details.save()
        fs = FileSystemStorage()
        storage_path = settings.BASE_DIR + \
            "/interactive_judge/media/problem_tests/" + str(prob_details.id)
        subprocess.call("mkdir " + storage_path, shell=True)
        fs.save(storage_path + "/interactor", request.FILES['interactor'])
        prob_details.interactor = storage_path + "/interactor"

        fs.save(storage_path + "/sample_input", request.FILES['input_file'])
        prob_details.sample_input = storage_path + "/sample_input"

        fs.save(storage_path + "/sample_output", request.FILES['output_file'])
        prob_details.sample_output = storage_path + "/sample_output"
        prob_details.save()
        return redirect('practice')

    return render(request, 'add_problems.html')
