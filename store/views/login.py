from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        postData = request.POST
        email = postData.get('email')
        password = postData.get('password')

        # Validation
        error_message = None

        if not email or not password:
            error_message = "Please fill out all fields."
        else:
            try:
                customer = Customer.objects.get(email=email)
                # Compare the plain-text password
                if password == customer.password:  # Compare plain-text password
                    request.session['customer'] = customer.id
                    return redirect('store')  # Redirect to the store page after successful login
                else:
                    error_message = "Invalid credentials. Please try again."
            except Customer.DoesNotExist:
                error_message = "Email not registered. Please sign up."

        data = {
            'error': error_message,
            'email': email
        }
        return render(request, 'login.html', data)



def logout(request):
    request.session.clear()
    return redirect('login')