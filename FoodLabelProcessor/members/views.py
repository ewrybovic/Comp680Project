from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print("test test test")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("Frontend/home.html")
        else:
            messages.success(request, ("Login error, verify username & password"))
            return redirect("login")
    else:
        return render(request, "authenticate/login.html", {})
