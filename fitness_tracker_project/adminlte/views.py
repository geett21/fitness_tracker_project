from django.shortcuts import render



def base(request):
    return render(request, 'base.html') 
def profile(request):
    return render(request, 'profile.html')  
