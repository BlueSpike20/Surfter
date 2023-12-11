from django.shortcuts import render

# Create your views here.
def surfting(request):
    return render(request, 'surfting/surfting.html')