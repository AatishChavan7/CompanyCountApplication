from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer
from .forms import UploadFileForm
from .tasks import process_csv
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

def base_view(request):
    return render(request, "company/base.html")

def login_view(request):
    print("Login view accessed")
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            error_message = 'Please provide the correct username and password.'

    # Render the login page with error message if applicable
    return render(request, 'company/login.html', {'error_message': error_message})

class CompanyQueryView(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = Company.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

@login_required
def upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            company_file = form.save()
            process_csv.delay(company_file.file.path)
            messages.success(request, 'Your file was successfully uploaded.')
            return redirect('upload')
    else:
        form = UploadFileForm()
    return render(request, 'company/upload.html', {'form': form})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'company/register.html', {'error': 'Username already exists'})
            else:
                user = CustomUser.objects.create_user(username=username, password=password1)
                if user is None:
                    return render(request, 'company/register.html', {'error': 'User creation failed'})
                return redirect('index')
        else:
            return render(request, 'company/register.html', {'error': 'Passwords do not match'})
    
    return render(request, 'company/register.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    return render(request, 'company/dashboard.html')

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CompanyQueryView(generics.ListAPIView):
    serializer_class = CompanySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Company.objects.all()
        params = {
            'name': 'name__icontains',
            'domain': 'domain__icontains',
            'year_founded': 'year_founded',
            'industry': 'industry__icontains',
            'locality': 'locality__icontains',
            'country': 'country__icontains',
            'employees_from': 'current_employee_estimate__gte',
            'employees_to': 'current_employee_estimate__lte'
        }

        for param, lookup in params.items():
            value = self.request.query_params.get(param, None)
            if value:
                queryset = queryset.filter(**{lookup: value})

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
            return Response({
                'count': queryset.count(),
                'next': response_data.get('next'),
                'previous': response_data.get('previous'),
                'results': response_data.get('results')
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })