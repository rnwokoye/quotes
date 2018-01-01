from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from . models import User, Quotes
from django.contrib import messages

# Create your views here.
def index(request):
	
	return render(request, "quotes/index.html")

def register(request):
	response = User.objects.register(
		request.POST["name"],
		request.POST["alias"],
		request.POST["email"],
		request.POST["dob"],
		request.POST["password"],
		request.POST["confirm"]
	)
	print response
	if response["valid"]:
		request.session["user_id"] = response["user"].id
		return redirect("/quotes")
	else:
		for error_message in response["errors"]:
			messages.add_message(request, messages.ERROR, error_message)
		return redirect("/")

def login(request):
	print '*' * 50
	response = User.objects.login(
		request.POST["email"],
		request.POST["password"]
	)
	print response
	if response["valid"]:
		request.session["user_id"] = response["user"].id
		return redirect("/quotes")
	else:
		for error_message in response["errors"]:
			messages.add_message(request, messages.ERROR, error_message)
		return redirect("/")

def quotes(request):
	if "user_id" not in request.session:
		return redirect("/")

	loggedin_user = User.objects.get(id=request.session["user_id"])
	favorite_quotes = Quotes.objects.filter(quotes_participant=loggedin_user)

	context = {
		"user": User.objects.get(id=request.session["user_id"]), 
		"all_users": User.objects.all().exclude(id=request.session["user_id"]),
		"quotable_quotes": Quotes.objects.exclude(quotes_participant=loggedin_user),
		"Favs" : favorite_quotes
	}
	return render(request, "quotes/quotes.html", context)

def logout(request):
	request.session.flush()
	return redirect("/")

def add_quote(request):
	loggedin_user = User.objects.get(id=request.session["user_id"])

	new_quote = Quotes.objects.create(quoted_by=request.POST["quoted_by"],content=request.POST["content"], posted_by=loggedin_user)

	return redirect("/quotes")

def add_favs(request, quote_id):
	# print "quote id is:...", quote_id

	favorited_quote = Quotes.objects.get(id=quote_id)
	loggedin_user = User.objects.get(id=request.session["user_id"])
	favorited_quote.quotes_participant.add(loggedin_user)

	return redirect("/quotes")

def remove_fav(request, quote_id):
	
	favorited_quote = Quotes.objects.get(id=quote_id)
	loggedin_user = User.objects.get(id=request.session["user_id"])
	favorited_quote.quotes_participant.remove(loggedin_user)

	return redirect("/quotes")
	
def user(request, user_id):

	user = User.objects.get(id=user_id)
	quotes = Quotes.objects.filter(posted_by=user_id)
	count = Quotes.objects.filter(posted_by=user_id).count()

	context = {
	"user": User.objects.get(id=user_id),
	"my_quotes": quotes,
	"count" : count
	}

	return render(request, "quotes/users.html", context)

