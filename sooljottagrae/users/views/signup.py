from django.contrib import messages
from django.contrib.auth import get_user_model

from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from users.forms import SignupForm


class SignupView(View):

    def get(self, request, *args, **kwargs):
        signupform = SignupForm()
        return render(
            request,
            "users/signup.html",
            {"signupform": signupform},
        )

    def post(self, request, *args, **kwargs):
        signupform = SignupForm()
        if request.method == "POST":
            signupform = SignupForm(request.POST, request.FILES)
            if signupform.is_valid():
                user = signupform.save(commit=False)
                user.email = signupform.cleaned_data['email']
                user.save()

                return HttpResponseRedirect(
                        reverse("users:login")
                )

        return render(
            request,
            "users/signup.html",
            {"signupform": signupform},
        )
