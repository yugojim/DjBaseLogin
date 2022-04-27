from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import pandas as pd
from . import Function
import pathlib
#from django.template import loader
from .models import Question,Choice

DataPath = pathlib.Path().absolute()
#print(pathlib.Path().absolute())
risk = str(DataPath) + '/risk.csv'
riskdf = pd.read_csv(risk, encoding='utf8')
#print(riskdf)

fhir = 'http://192.168.1.119:8001/fhir/'
def index(request):
    try:
        if 'PatientID' in request.POST:
            PatientID = request.POST['PatientID']
            context=Function.post_data(fhir,PatientID)
            #print(context)
        else:
            PatientID=None
        return render(request, 'geneticsVghtc.html', context)
    except:
        return render(request, 'geneticsVghtc.html')

def dbSNP(request):
    try:
        if 'Alleles' in request.POST:
            Alleles = request.POST['Alleles']
            dbSNP = request.POST['dbSNP']
            #print(Alleles)
            context=Function.post_dbSNP(fhir,Alleles,dbSNP)
            #print(context)
        elif 'Alleles' in request.GET:
            Alleles = request.GET['Alleles']
            dbSNP = request.GET['dbSNP']
            #print(Alleles)
            context=Function.post_dbSNP(fhir,Alleles,dbSNP)
        else:
            context=None
        return render(request, 'geneticsdbSNP.html', context)
    except:
        return render(request, 'geneticsdbSNP.html')

def getRisk(request):
    try:
        riskrlue = request.GET['risk']
        #riskrlue='Alc_risk'
        #print(riskrlue)

        risksdf=riskdf[riskdf['risk']==riskrlue]
        #print(risksdf)
        #risksdict = risksdf.to_dict()
        risksdict = risksdf.to_dict('records')
    
        context = {
                'riskrlue' : riskrlue,
                'risks' : risksdict
                }
        return render(request,'geneticsRisk.html', context)
    except:
        return render(request,'geneticsRisk.html')

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