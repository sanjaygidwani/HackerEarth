from django.db import models

class Problems(models.Model):
    NOTHING = 0
    USERINPUT = 1
    INTERACTORINPUT = 2
    BOTH = 3
    TYPE_CHOICES = (
        (NOTHING, 'Nothing'),
        (USERINPUT, 'UserInput'),
        (INTERACTORINPUT, 'InteractorInput'),
        (BOTH, 'Both'),
    )

    prob_description = models.TextField()
    sample_input = models.CharField(max_length=200)
    sample_output = models.CharField(max_length=200)
    sample_exp = models.TextField()
    interactor = models.CharField(max_length=200)
    prob_title = models.CharField(max_length=100)
    time_limit = models.IntegerField(default = 1)
    memory_limit = models.IntegerField(default = 256)
    input_type = models.IntegerField(choices=TYPE_CHOICES,default=NOTHING,)

class Submissions(models.Model):
    username = models.ForeignKey('auth.User',on_delete= models.CASCADE)
    pid = models.ForeignKey('interactive_judge.Problems',on_delete=models.CASCADE)

class TestCase(models.Model):
    pid = models.ForeignKey('interactive_judge.Problems', on_delete=models.CASCADE)
    testfile_user = models.CharField(max_length=100,default=None,null=True,blank=True)
    testfile_interactor = models.CharField(max_length=100,default = None,null=True,blank=True)
    score = models.IntegerField(default=0)

class ProblemSubmission(models.Model):
    AC = 0
    WA = 1
    TLE = 2
    # Compilation error in user code
    CEU = 3
    # Compilation error in interactor code
    CEI = 4
    # Server error (pipe not being created etc.)
    SE = 5
    VERDICT_POSSIBILITIES = (
        (AC, 'Ac'),
        (WA, 'Wa'),
        (TLE, 'Tle'),
        (CEU, 'Ceu'),
        (CEI, 'Cei'),
        (SE, 'Se'),
    )

    pid = models.ForeignKey('interactive_judge.Problems', on_delete=models.CASCADE)
    sid = models.ForeignKey('interactive_judge.Submissions', on_delete=models.CASCADE)
    memory = models.IntegerField()
    time = models.DecimalField(decimal_places=5,max_digits=7)
    testid = models.ForeignKey('interactive_judge.TestCase', on_delete=models.CASCADE)
    verdict = models.IntegerField(choices=VERDICT_POSSIBILITIES,)


