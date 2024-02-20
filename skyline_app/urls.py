# This Is From and Improt ----------------

from django.urls import path
from skyline_app import views
from django.conf.urls.static import static
from skyline import settings


# This is Urlpatterns For Page------------

urlpatterns = [
    path('about',views.about),
    path('home',views.home),
    path('edit/<rid>',views.edit),
    path('delete/<rid>',views.delete),
    path('myview',views.SimpleViews.as_view()),
    path('pdetails/<pid>',views.product_details),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail/<uname>',views.send_mail),
]




# This Is Debug Settings-----------------------

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)