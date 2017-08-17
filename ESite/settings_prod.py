# import os
from .settings_base import *



ALLOWED_HOSTS = [
    'localhost'
]

INSTALLED_APPS += (

)
    

MIDDLEWARE = (
    'django.middleware.cache.UpdateCacheMiddleware',
) + MIDDLEWARE + (
    'django.middleware.cache.FetchFromCacheMiddleware',
)



SECRET_KEY = os.environ.get('SECRET_KEY') or 'sadyugfh513 5gdx4r84g13xdf gx3df5g1 x35d1'



DEBUG = False

# CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True

# STATIC_ROOT =  os.path.join(BASE_DIR, "staticfile/")

# Alternatively the redis connection can be defined using a URL:
CACHEOPS_REDIS = "redis://localhost:6379/1"


CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This includes request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    # 'auth.user': {'ops': 'get', 'timeout': 60*15},

    # # Automatically cache all gets and queryset fetches
    # # to other django.contrib.auth models for an hour

    
    'hitcount.*': {'ops': ('all'), 'timeout': 60*60, 'cache_on_save': True},
    'econ.*': {'ops': 'all', 'timeout': 60*60, 'cache_on_save': True},

    # Cache all queries to Permission
    # 'all' is just an alias for {'get', 'fetch', 'count', 'aggregate', 'exists'}
    # 'auth.permission': {'ops': 'all', 'timeout': 60*60},

    # # Enable manual caching on all other models with default timeout of an hour
    # # Use Post.objects.cache().get(...)
    # #  or Tags.objects.filter(...).order_by(...).cache()
    # # to cache particular ORM request.
    # # Invalidation is still automatic
    # '*.*': {'ops': (), 'timeout': 60*60},

    # # And since ops is empty by default you can rewrite last line as:
    '*.*': {'timeout': 60*60},
    
}
