from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()


class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extrcating token from query params
        query_string = scope.get('query_string', b'').decode()
        token = dict(q.split('=') for q in query_string.split('&') if q).get('token', None)

        if token:
            scope['user'] = await self.get_user(token)
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            return User.objects.get(auth_token=token)
        except User.DoesNotExist:
            return AnonymousUser()
