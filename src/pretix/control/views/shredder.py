import logging
from collections import OrderedDict

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import TemplateView

from pretix.base.models import CachedFile
from pretix.base.services.shredder import export, shred
from pretix.base.shredder import shred_constraints
from pretix.base.views.async import AsyncAction
from pretix.control.permissions import EventPermissionRequiredMixin

logger = logging.getLogger(__name__)


class ShredderMixin:

    @cached_property
    def shredders(self):
        return OrderedDict(
            sorted(self.request.event.get_data_shredders().items(), key=lambda s: s[1].verbose_name)
        )


class StartShredView(EventPermissionRequiredMixin, ShredderMixin, TemplateView):
    permission = 'can_change_orders'
    template_name = 'pretixcontrol/shredder/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['shredders'] = self.shredders
        ctx['constraints'] = shred_constraints(self.request.event)
        return ctx


class ShredDownloadView(EventPermissionRequiredMixin, ShredderMixin, TemplateView):
    permission = 'can_change_orders'
    template_name = 'pretixcontrol/shredder/download.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['shredders'] = self.shredders
        ctx['file'] = get_object_or_404(CachedFile, pk=kwargs.get("file"))
        return ctx


class ShredExportView(EventPermissionRequiredMixin, ShredderMixin, AsyncAction, View):
    permission = 'can_change_orders'
    task = export

    def get_success_message(self, value):
        return None

    def get_success_url(self, value):
        return reverse('control:event.shredder.download', kwargs={
            'event': self.request.event.slug,
            'organizer': self.request.event.organizer.slug,
            'file': str(value)
        })

    def get_error_url(self):
        return reverse('control:event.shredder.start', kwargs={
            'event': self.request.event.slug,
            'organizer': self.request.event.organizer.slug
        })

    def post(self, request, *args, **kwargs):
        if shred_constraints(self.request.event):
            return redirect(self.get_error_url())

        return self.do(self.request.event.id, request.POST.getlist("shredder"))


class ShredDoView(EventPermissionRequiredMixin, ShredderMixin, AsyncAction, View):
    permission = 'can_change_orders'
    task = shred

    def get_success_message(self, value):
        return None

    def get_success_url(self, value):
        return reverse('control:event.shredder.start', kwargs={
            'event': self.request.event.slug,
            'organizer': self.request.event.organizer.slug,
        })

    def get_error_url(self):
        return reverse('control:event.shredder.start', kwargs={
            'event': self.request.event.slug,
            'organizer': self.request.event.organizer.slug
        })

    def post(self, request, *args, **kwargs):
        if shred_constraints(self.request.event):
            return redirect(self.get_error_url())

        return self.do(self.request.event.id, request.POST.get("file"))