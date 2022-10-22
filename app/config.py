from app.services.apilayer.settings import ApiLayerSettings
from .containers import ApplicationContainer


app_container = ApplicationContainer()

apilayer_settings = ApiLayerSettings()

settings = app_container.settings()

app_container.config.from_dict({
    'apilayer': {
        'api_key': apilayer_settings.APILAYER_API_KEY,
        'connection_timeout': apilayer_settings.APILAYER_CONNECTION_TIMEOUT,
    },
    'converter_type': settings.CONVERTER_TYPE
})
