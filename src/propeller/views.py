from django.conf import settings
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse, Http404, HttpResponseRedirect
#from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
#from django.shortcuts import redirect
from django.template import RequestContext

@login_required
def index(request):
    return render_to_response('document/index.html', {'request': request,
                                                    }, context_instance=RequestContext(request))
