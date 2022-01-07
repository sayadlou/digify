from .base import *

import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from .base import urlpatterns

urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),

]