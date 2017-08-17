from .settings_base import *



DEBUG = True


ALLOWED_HOSTS = []


INSTALLED_APPS += (
    'debug_toolbar',
    'template_timings_panel',
)
    

MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

) + MIDDLEWARE


INTERNAL_IPS=('127.0.0.1',)


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
]

GRAPHENE = {
    'SCHEMA': 'econ.schema.schema', # Where your Graphene schema lives
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
    ]
}


# CACHEOPS_REDIS = "redis://localhost:6379/1"


# CACHEOPS = {
#     'hitcount.*': {'ops': ('all'), 'timeout': 60*60, 'cache_on_save': True},
#     'econ.*': {'ops': 'all', 'timeout': 60*60, 'cache_on_save': True},
#     '*.*': {'timeout': 60*60},
# }
