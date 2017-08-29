from django.shortcuts import render
from .models import Question, Choice
from random import randint

def index(request):
	question_list = Question.objects.all()
	for question in question_list:
		question.has_voted_on = False
		question.save()
	question = question_list[randint(0, question_list.count() - 1)]
	choices = Choice.objects.filter(question=question)
	context = {'question': question, 'choices': choices}
	return render(request, 'detail.html', context)

def detail(request, question_id):
	question = Question.objects.get(pk=question_id)
	choices = Choice.objects.filter(question=question)
	context = {'question': question, 'choices': choices}
	return render(request, 'detail.html', context)

def vote(request, question_id):
	question = Question.objects.get(pk=question_id)
	try: 
		choice = question.choice_set.get(pk=request.POST['choice'])
	except:
		choices = Choice.objects.filter(question=question)
		context = {'question': question, 'choices': choices, 'error_message': 'You did not select a choice'}
		return render(request, 'detail.html', context)
	else:
		choice.votes += 1
		choice.save()
		question_list = Question.objects.all().exclude(pk=question_id)
		context = {'question_list': question_list}
		return render(request, 'index.html', context) 

