
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from store.forms import StaffLoginForm
from django.views import View

class StaffLoginView(View):
    def get(self, request):
        form = StaffLoginForm()
        return render(request, 'staff_login.html', {'form': form})

    def post(self, request):
        form = StaffLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('backoffice')  # Redirect to the backoffice page after successful login
            else:
                messages.error(request, 'Invalid username or password')
        return render(request, 'staff_login.html', {'form': form})
