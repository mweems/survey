from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Question, Choice
from random import randint

def index(request):
	question_list = Question.objects.all()
	for question in question_list:
		question.has_voted_on = False
		question.save()
	context = get_random_question(question_list)
	if not context:
		return render(request, 'finished.html')
	return render(request, 'detail.html', context)

def myLogin(request):
	if request.method == 'POST':
		logout(request)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			return redirect('adminPage')
		else:
			return render(request, 'login.html', {'error_message': 'Incorrect user name or password'})

	return render(request, 'login.html')

def deleteQuestion(request):
	try:
		Question.objects.filter(pk=request.POST['question']).delete()
	except:
		question_list = Question.objects.all()
		choices = Choice.objects.all()
		context = {'questions': question_list, 'choices': choices, 'error_message': 'You must select a question to delete it'}
		return render(request, 'adminPage.html', context)
	return redirect('adminPage')

def addQuestion(request):
	Question.objects.create(question_text=request.POST['question'])
	return redirect('adminPage')

def addChoice(request):
	try:
		question = Question.objects.get(pk=request.POST['question'])
		Choice.objects.create(question=question, choice_text=request.POST['choice'])
	except:
		question_list = Question.objects.all()
		choices = Choice.objects.all()
		context = {'questions': question_list, 'choices': choices, 'error_message': 'You must select a question to add a choice'}
		return render(request, 'adminPage.html', context)

	return redirect('adminPage')

def deleteChoice(request):
	try:
		Choice.objects.filter(pk=request.POST['choice']).delete()
	except:
		question_list = Question.objects.all()
		choices = Choice.objects.all()
		context = {'questions': question_list, 'choices': choices, 'error_message': 'You must select a choice to delete it'}
		return render(request, 'adminPage.html', context)

	return redirect('adminPage')

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
		return render(request, 'detail.html', {'question': question, 'error_message': 'Please select an option'})
	choice.votes += 1
	choice.save()
	question.has_voted_on = True
	question.save()
	question_list = Question.objects.all().exclude(has_voted_on=True)
	context = get_random_question(question_list)
	if not context:
		return render(request, 'finished.html')
	return render(request, 'detail.html', context)

def adminPage(request):
	question_list = Question.objects.all()
	choices = Choice.objects.all()
	context = {'questions': question_list, 'choices': choices}
	return render(request, 'adminPage.html', context)


def get_random_question(question_list):
	if not question_list:
		return None
	question = question_list[randint(0, question_list.count() - 1)]
	choices = Choice.objects.filter(question=question)
	return {'question': question, 'choices': choices}


