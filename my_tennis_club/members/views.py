from django.shortcuts import render, get_object_or_404
from .models import Members

def main(request):
    return render(request, 'main.html')

def members(request):
    mymembers = Members.objects.all()
    return render(request, 'all_members.html', {'mymembers': mymembers})

def details(request, id):
    mymember = get_object_or_404(Members, id=id)
    return render(request, 'details.html', {'mymember': mymember})
