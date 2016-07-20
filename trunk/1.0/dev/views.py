from celery.result import AsyncResult
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from dev.tasks import do_work

def poll_state(request):
	print "$$$$$$$$"
	""" A view to report the progress to the user """
	if 'job' in request.GET:
		job_id = request.GET['job']
	else:
		return HttpResponse('No job id given.')
	job = AsyncResult(job_id)
	data = job.result or job.state
	return HttpResponse(json.dumps(data), mimetype='application/json')
def init_work(request):
	""" A view to start a background job and redirect to the status page """
	job = do_work.delay()
	# return HttpResponseRedirect(reverse('dev.views.poll_state',kwargs={'job':job.id}))
	return HttpResponseRedirect(reverse('poll_state' + '?job=' + job.id))