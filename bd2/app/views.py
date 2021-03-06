from django.http import HttpResponse

from django.template import loader
from django.views import generic
from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Q
from app.models import *
from app import forms
# Create your views here.

def index(request):
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render({}, request))

class WorkerListView(generic.ListView):
    model = Worker
    context_object_name = 'workers'
    template_name = 'app/workers.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(supervisor__id=self.request.user.id)
        return queryset

class WorkerDetailView(generic.DetailView):
    model = Worker
    context_object_name = 'worker'
    template_name = 'app/worker.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(supervisor__id=self.request.user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['date'] = ("{}".format(context['worker'].employment_date))
        context['logs'] = LogEntry.objects.filter(
            (Q(subbed=context['worker']) | Q(subbing=context['worker']))
        )
        return self.render_to_response(context)

class SubListView(generic.ListView):
    model = Substitution
    context_object_name = 'subs'
    queryset = Substitution.objects.all()
    template_name = 'app/subs.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(substituted_worker__supervisor__id=self.request.user.id)
        return queryset

class SubDetailView(generic.DetailView):
    model = Substitution
    context_object_name = 'sub'
    template_name = 'app/sub.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(substituted_worker__supervisor__id=self.request.user.id)
        return queryset

    def sub_detail_view(request, primary_key):
        try:
            sub = Substitution.objects.get(pk=primary_key)
        except Substitution.DoesNotExist:
            raise Http404('Worker does not exist')

        return render(request, 'catalog/worker.html', context={'sub': sub})

class SubCreateView(generic.CreateView):
    model = Substitution
    template_name = 'app/postsub.html'
    success_url = reverse_lazy('sub_list')
    form_class = forms.SubstitutionForm

    def get_form_class(self):
        form = super().get_form_class()
        print(form.__dict__)

        form.base_fields['substituted_worker'].queryset = Worker.objects.filter(supervisor=self.request.user)
        form.base_fields['substituting_worker'].queryset = Worker.objects.filter(supervisor=self.request.user)

        return form

class SubDeleteView(generic.DeleteView):
    model = Substitution
    template_name = 'app/deletesub.html'
    success_url = reverse_lazy('sub_list')

class LogListView(generic.ListView):
    model = LogEntry
    context_object_name = 'logs'
    queryset = LogEntry.objects.all()
    template_name = 'app/logs.html'

class LogDetailView(generic.DetailView):
    model = LogEntry
    context_object_name = 'log'
    template_name = 'app/log.html'

    def worker_detail_view(request, primary_key):
        try:
            log = LogEntry.objects.get(pk=primary_key)
        except LogEntry.DoesNotExist:
            raise Http404('Worker does not exist')

        return render(request, 'catalog/log.html', context={'log': log})
