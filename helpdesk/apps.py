from django.apps import AppConfig


class HelpdeskConfig(AppConfig):
    name = 'helpdesk'
    verbose_name = "Helpdesk"

    def ready(self):
        import helpdesk.signals
