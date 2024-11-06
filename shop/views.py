from django.views.generic import TemplateView

class WebSocketTestView(TemplateView):
    template_name = 'shop/websocket_test.html'