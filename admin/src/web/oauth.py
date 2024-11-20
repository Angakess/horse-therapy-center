from oauthlib.oauth2 import WebApplicationClient


class OAuth:
    def __init__(self, app=None):
        self._client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Inicializa el cliente de oAuth y lo adjunta al contexto de la app"""
        self._google_client_id = app.config.get("GOOGLE_CLIENT_ID")
        self._google_client_secret = app.config.get("GOOGLE_CLIENT_SECRET")
        self._google_discovery_url = app.config.get("GOOGLE_DISCOVERY_URL")

        self._client = WebApplicationClient(self.google_client_id)

        app.oauth = self

        return app

    @property
    def client(self):
        """Propiedad para obtener el cliente de oAuth"""
        return self._client

    @client.setter
    def client(self, value):
        """Propiedad setter para permitir reasignar el cliente de oAuth"""
        self._client = value

    @property
    def discovery_url(self):
        return self._google_discovery_url

    @property
    def google_client_id(self):
        return self._google_client_id

    @property
    def google_client_secret(self):
        return self._google_client_secret


oauth = OAuth()
