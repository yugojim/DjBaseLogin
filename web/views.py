from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
#from django.template import loader

from .models import Question,Choice

def index(request):
    if 'PatientID' in request.POST:
        PatientID = request.POST['PatientID']
    else:
        PatientID=None
    HBBlist=[]
    Obes_list=[]
    ABCG2list=[]
    ALDH2list=[]
    NOTCH3list=[]
    LDLRlist=[]
    CYP2C19list=[]
    HBB_risk=[]
    Obes_risk=[]
    FH_risk=[]
    final_comment=[]
    context = {
        'PatientID' : PatientID,
        'ALDH2list' : ALDH2list,
        'Obes_list' : Obes_list,
        'ABCG2list' : ABCG2list,
        'HBBlist' : HBBlist,
        'LDLRlist' : LDLRlist,
        'NOTCH3list' : NOTCH3list,
        'CYP2C19list' : CYP2C19list,
        'HBB_risk' : HBB_risk,
        'Obes_risk' : Obes_risk,
        'FH_risk' : FH_risk,
        'final_comment' : final_comment,
        }
    return render(request, 'geneticsVghtc.html', context)


############
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('web:results', args=(question.id,)))