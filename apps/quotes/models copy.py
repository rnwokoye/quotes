# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, name, alias, email, dob, password, confirm):
		response = {
			"valid": True,
			"errors": [],
			"user": None
		}

		if len(name) < 1:
			response["errors"].append("Name is required")
		elif len(name) < 3:
			response["errors"].append("Name must be 3 characters or longer")

		if len(alias) < 1:
			response["errors"].append("Alias is required")
		elif len(alias) < 3:
			response["errors"].append("Alias must be 3 characters or longer")

		if len(email) < 1:
			response["errors"].append("Email is required")
		elif not EMAIL_REGEX.match(email):
			response["errors"].append("Invalid Email")
		else:
			email_list = User.objects.filter(email=email.lower())
			if len(email_list) > 0:
				response["errors"].append("Email is already in use")

		if len(dob) < 1:
			response["errors"].append("Date of Birth is required")
		else:
			date = datetime.strptime(dob, '%Y-%m-%d')
			today = datetime.now()
			if date > today:
				response["errors"].append("Date of Birth must be in the past")

		if len(password) < 1:
			response["errors"].append("Password is required")
		elif len(password) < 8:
			response["errors"].append("Password must be 8 characters or longer")

		if len(confirm) < 1:
			response["errors"].append("Confirm Password is required")
		elif confirm != password:
			response["errors"].append("Confirm Password must match Password")

		if len(response["errors"]) > 0:
			response["valid"] = False
		else:
			response["user"] = User.objects.create(
				name=name,
				alias=alias,
				email=email.lower(),
				dob=date,
				password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			)
		return response

	def login(self, email, password):
		response = {
			"valid": True,
			"errors": [],
			"user": None
		}

		if len(email) < 1:
			response["errors"].append("Email is required")
		elif not EMAIL_REGEX.match(email):
			response["errors"].append("Invalid Email")
		else:
			email_list = User.objects.filter(email=email.lower())
			if len(email_list) == 0:
				response["errors"].append("Email not found!")

		if len(password) < 8:
			response["errors"].append("Password must be 8 characters or longer")

		if len(response["errors"]) == 0:
			hashed_pw = email_list[0].password
			if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
				response["user"] = email_list[0]
			else:
				response["errors"].append("Incorrect Password")

		if len(response["errors"]) > 0:
			response["valid"] = False

		return response


class QuoteManager(models.Manager):
	def postQuote(self, content, quoted_by, posted_by):
		response = {
			"valid": True,
			errors: [],
			quoted_by: None
		}

		if len(quoted_by) < 3:
			response["errors"].append("'quoted_by' must be more than 3 characters!")

		if len(content) < 10:
			response["errors"].append("'content' must be more than 3 characters!")

		if len(response["errors"]) > 0:
			response["valid"] = False

		else:
			response["quoted_by"] = Quotes.objects.create(		#changed quote to quoted_by last change
				content=content,
				quoted_by=quoted_by,
				posted_by=user_posts
			)
		return response 


class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	dob = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Quotes(models.Model):
	content = models.TextField(max_length=1000)
	quoted_by = models.TextField(max_length=1000)
	posted_by = models.ForeignKey(User, related_name="user_posts")
	quotes_participant = models.ManyToManyField(User, related_name="favorite")
	posted_at = models.DateTimeField(auto_now_add=True)
	objects = QuoteManager()

