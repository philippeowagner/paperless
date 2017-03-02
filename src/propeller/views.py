from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    context = {}
    return render(request, 'docs/index.html', context)
