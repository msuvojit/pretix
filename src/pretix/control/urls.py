from django.conf.urls import include, url

from pretix.control.views import (
    auth, checkin, dashboards, event, global_settings, item, main, orders,
    organizer, search, subevents, typeahead, user, vouchers, waitinglist,
)

urlpatterns = [
    url(r'^logout$', auth.logout, name='auth.logout'),
    url(r'^login$', auth.login, name='auth.login'),
    url(r'^login/2fa$', auth.Login2FAView.as_view(), name='auth.login.2fa'),
    url(r'^register$', auth.register, name='auth.register'),
    url(r'^invite/(?P<token>[a-zA-Z0-9]+)$', auth.invite, name='auth.invite'),
    url(r'^forgot$', auth.Forgot.as_view(), name='auth.forgot'),
    url(r'^forgot/recover$', auth.Recover.as_view(), name='auth.forgot.recover'),
    url(r'^$', dashboards.user_index, name='index'),
    url(r'^global/settings/$', global_settings.GlobalSettingsView.as_view(), name='global.settings'),
    url(r'^global/update/$', global_settings.UpdateCheckView.as_view(), name='global.update'),
    url(r'^reauth/$', user.ReauthView.as_view(), name='user.reauth'),
    url(r'^settings/?$', user.UserSettings.as_view(), name='user.settings'),
    url(r'^settings/2fa/$', user.User2FAMainView.as_view(), name='user.settings.2fa'),
    url(r'^settings/history/$', user.UserHistoryView.as_view(), name='user.settings.history'),
    url(r'^settings/2fa/add$', user.User2FADeviceAddView.as_view(), name='user.settings.2fa.add'),
    url(r'^settings/2fa/enable', user.User2FAEnableView.as_view(), name='user.settings.2fa.enable'),
    url(r'^settings/2fa/disable', user.User2FADisableView.as_view(), name='user.settings.2fa.disable'),
    url(r'^settings/2fa/regenemergency', user.User2FARegenerateEmergencyView.as_view(),
        name='user.settings.2fa.regenemergency'),
    url(r'^settings/2fa/totp/(?P<device>[0-9]+)/confirm', user.User2FADeviceConfirmTOTPView.as_view(),
        name='user.settings.2fa.confirm.totp'),
    url(r'^settings/2fa/u2f/(?P<device>[0-9]+)/confirm', user.User2FADeviceConfirmU2FView.as_view(),
        name='user.settings.2fa.confirm.u2f'),
    url(r'^settings/2fa/(?P<devicetype>[^/]+)/(?P<device>[0-9]+)/delete', user.User2FADeviceDeleteView.as_view(),
        name='user.settings.2fa.delete'),
    url(r'^organizers/$', organizer.OrganizerList.as_view(), name='organizers'),
    url(r'^organizers/add$', organizer.OrganizerCreate.as_view(), name='organizers.add'),
    url(r'^organizer/(?P<organizer>[^/]+)/$', organizer.OrganizerDetail.as_view(), name='organizer'),
    url(r'^organizer/(?P<organizer>[^/]+)/edit$', organizer.OrganizerUpdate.as_view(), name='organizer.edit'),
    url(r'^organizer/(?P<organizer>[^/]+)/teams$', organizer.TeamListView.as_view(), name='organizer.teams'),
    url(r'^organizer/(?P<organizer>[^/]+)/team/add$', organizer.TeamCreateView.as_view(), name='organizer.team.add'),
    url(r'^organizer/(?P<organizer>[^/]+)/team/(?P<team>[^/]+)/$', organizer.TeamMemberView.as_view(),
        name='organizer.team'),
    url(r'^organizer/(?P<organizer>[^/]+)/team/(?P<team>[^/]+)/edit$', organizer.TeamUpdateView.as_view(),
        name='organizer.team.edit'),
    url(r'^organizer/(?P<organizer>[^/]+)/team/(?P<team>[^/]+)/delete$', organizer.TeamDeleteView.as_view(),
        name='organizer.team.delete'),
    url(r'^organizer/(?P<organizer>[^/]+)/slugrng', main.SlugRNG.as_view(), name='events.add.slugrng'),
    url(r'^events/$', main.EventList.as_view(), name='events'),
    url(r'^events/add$', main.EventWizard.as_view(), name='events.add'),
    url(r'^events/typeahead/$', typeahead.event_list, name='events.typeahead'),
    url(r'^search/orders/$', search.OrderSearch.as_view(), name='search.orders'),
    url(r'^event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/', include([
        url(r'^$', dashboards.event_index, name='event.index'),
        url(r'^live/$', event.EventLive.as_view(), name='event.live'),
        url(r'^logs/$', event.EventLog.as_view(), name='event.log'),
        url(r'^requiredactions/$', event.EventActions.as_view(), name='event.requiredactions'),
        url(r'^requiredactions/(?P<id>\d+)/discard$', event.EventActionDiscard.as_view(),
            name='event.requiredaction.discard'),
        url(r'^comment/$', event.EventComment.as_view(),
            name='event.comment'),
        url(r'^settings/$', event.EventUpdate.as_view(), name='event.settings'),
        url(r'^settings/plugins$', event.EventPlugins.as_view(), name='event.settings.plugins'),
        url(r'^settings/permissions$', event.EventPermissions.as_view(), name='event.settings.permissions'),
        url(r'^settings/payment$', event.PaymentSettings.as_view(), name='event.settings.payment'),
        url(r'^settings/tickets$', event.TicketSettings.as_view(), name='event.settings.tickets'),
        url(r'^settings/tickets/preview/(?P<output>[^/]+)$', event.TicketSettingsPreview.as_view(),
            name='event.settings.tickets.preview'),
        url(r'^settings/email$', event.MailSettings.as_view(), name='event.settings.mail'),
        url(r'^settings/email/preview$', event.MailSettingsPreview.as_view(), name='event.settings.mail.preview'),
        url(r'^settings/invoice$', event.InvoiceSettings.as_view(), name='event.settings.invoice'),
        url(r'^settings/invoice/preview$', event.InvoicePreview.as_view(), name='event.settings.invoice.preview'),
        url(r'^settings/display', event.DisplaySettings.as_view(), name='event.settings.display'),
        url(r'^subevents/$', subevents.SubEventList.as_view(), name='event.subevents'),
        url(r'^subevents/(?P<subevent>\d+)/$', subevents.SubEventUpdate.as_view(), name='event.subevent'),
        url(r'^subevents/(?P<subevent>\d+)/delete$', subevents.SubEventDelete.as_view(),
            name='event.subevent.delete'),
        url(r'^subevents/add$', subevents.SubEventCreate.as_view(), name='event.subevents.add'),
        url(r'^items/$', item.ItemList.as_view(), name='event.items'),
        url(r'^items/add$', item.ItemCreate.as_view(), name='event.items.add'),
        url(r'^items/(?P<item>\d+)/$', item.ItemUpdateGeneral.as_view(), name='event.item'),
        url(r'^items/(?P<item>\d+)/variations$', item.ItemVariations.as_view(),
            name='event.item.variations'),
        url(r'^items/(?P<item>\d+)/addons', item.ItemAddOns.as_view(),
            name='event.item.addons'),
        url(r'^items/(?P<item>\d+)/up$', item.item_move_up, name='event.items.up'),
        url(r'^items/(?P<item>\d+)/down$', item.item_move_down, name='event.items.down'),
        url(r'^items/(?P<item>\d+)/delete$', item.ItemDelete.as_view(), name='event.items.delete'),
        url(r'^categories/$', item.CategoryList.as_view(), name='event.items.categories'),
        url(r'^categories/(?P<category>\d+)/delete$', item.CategoryDelete.as_view(),
            name='event.items.categories.delete'),
        url(r'^categories/(?P<category>\d+)/up$', item.category_move_up, name='event.items.categories.up'),
        url(r'^categories/(?P<category>\d+)/down$', item.category_move_down,
            name='event.items.categories.down'),
        url(r'^categories/(?P<category>\d+)/$', item.CategoryUpdate.as_view(),
            name='event.items.categories.edit'),
        url(r'^categories/add$', item.CategoryCreate.as_view(), name='event.items.categories.add'),
        url(r'^questions/$', item.QuestionList.as_view(), name='event.items.questions'),
        url(r'^questions/(?P<question>\d+)/delete$', item.QuestionDelete.as_view(),
            name='event.items.questions.delete'),
        url(r'^questions/(?P<question>\d+)/up$', item.question_move_up, name='event.items.questions.up'),
        url(r'^questions/(?P<question>\d+)/down$', item.question_move_down,
            name='event.items.questions.down'),
        url(r'^questions/(?P<question>\d+)/$', item.QuestionView.as_view(),
            name='event.items.questions.show'),
        url(r'^questions/(?P<question>\d+)/change$', item.QuestionUpdate.as_view(),
            name='event.items.questions.edit'),
        url(r'^questions/add$', item.QuestionCreate.as_view(), name='event.items.questions.add'),
        url(r'^quotas/$', item.QuotaList.as_view(), name='event.items.quotas'),
        url(r'^quotas/(?P<quota>\d+)/$', item.QuotaView.as_view(), name='event.items.quotas.show'),
        url(r'^quotas/(?P<quota>\d+)/change$', item.QuotaUpdate.as_view(), name='event.items.quotas.edit'),
        url(r'^quotas/(?P<quota>\d+)/delete$', item.QuotaDelete.as_view(),
            name='event.items.quotas.delete'),
        url(r'^quotas/add$', item.QuotaCreate.as_view(), name='event.items.quotas.add'),
        url(r'^vouchers/$', vouchers.VoucherList.as_view(), name='event.vouchers'),
        url(r'^vouchers/tags/$', vouchers.VoucherTags.as_view(), name='event.vouchers.tags'),
        url(r'^vouchers/rng$', vouchers.VoucherRNG.as_view(), name='event.vouchers.rng'),
        url(r'^vouchers/(?P<voucher>\d+)/$', vouchers.VoucherUpdate.as_view(), name='event.voucher'),
        url(r'^vouchers/(?P<voucher>\d+)/delete$', vouchers.VoucherDelete.as_view(),
            name='event.voucher.delete'),
        url(r'^vouchers/add$', vouchers.VoucherCreate.as_view(), name='event.vouchers.add'),
        url(r'^vouchers/bulk_add$', vouchers.VoucherBulkCreate.as_view(), name='event.vouchers.bulk'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/transition$', orders.OrderTransition.as_view(),
            name='event.order.transition'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/resend$', orders.OrderResendLink.as_view(),
            name='event.order.resendlink'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/invoice$', orders.OrderInvoiceCreate.as_view(),
            name='event.order.geninvoice'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/invoices/(?P<id>\d+)/regenerate$', orders.OrderInvoiceRegenerate.as_view(),
            name='event.order.regeninvoice'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/invoices/(?P<id>\d+)/reissue$', orders.OrderInvoiceReissue.as_view(),
            name='event.order.reissueinvoice'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/answer/(?P<answer>[^/]+)/$',
            orders.AnswerDownload.as_view(),
            name='event.order.download.answer'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/extend$', orders.OrderExtend.as_view(),
            name='event.order.extend'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/contact$', orders.OrderContactChange.as_view(),
            name='event.order.contact'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/locale', orders.OrderLocaleChange.as_view(),
            name='event.order.locale'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/comment$', orders.OrderComment.as_view(),
            name='event.order.comment'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/change$', orders.OrderChange.as_view(),
            name='event.order.change'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/sendmail$', orders.OrderSendMail.as_view(),
            name='event.order.sendmail'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/mail_history$', orders.OrderEmailHistory.as_view(),
            name='event.order.mail_history'),
        url(r'^orders/(?P<code>[0-9A-Z]+)/$', orders.OrderDetail.as_view(), name='event.order'),
        url(r'^invoice/(?P<invoice>[^/]+)$', orders.InvoiceDownload.as_view(),
            name='event.invoice.download'),
        url(r'^orders/overview/$', orders.OverView.as_view(), name='event.orders.overview'),
        url(r'^orders/export/$', orders.ExportView.as_view(), name='event.orders.export'),
        url(r'^orders/export/do$', orders.ExportDoView.as_view(), name='event.orders.export.do'),
        url(r'^orders/go$', orders.OrderGo.as_view(), name='event.orders.go'),
        url(r'^orders/$', orders.OrderList.as_view(), name='event.orders'),
        url(r'^waitinglist/$', waitinglist.WaitingListView.as_view(), name='event.orders.waitinglist'),
        url(r'^waitinglist/auto_assign$', waitinglist.AutoAssign.as_view(), name='event.orders.waitinglist.auto'),
        url(r'^waitinglist/(?P<entry>\d+)/delete$', waitinglist.EntryDelete.as_view(), name='event.orders.waitinglist.delete'),
        url(r'^checkins/$', checkin.CheckInView.as_view(), name='event.orders.checkins'),
    ])),
]
