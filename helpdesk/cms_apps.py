from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class HelpdeskApphook(CMSApp):
    app_name = "helpdesk"
    name = _("Helpdesk Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["helpdesk.urls"]


apphook_pool.register(HelpdeskApphook)
