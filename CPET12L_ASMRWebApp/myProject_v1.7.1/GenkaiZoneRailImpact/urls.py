from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import sign_out
from . import views

urlpatterns = [
    path('Admin',views.Admin,name='Admin'),
    path('process_application',views.process_application,name='process_application'),
    path('Receive',views.goto_receive,name='Receive'),
    path('do_tag_receive',views.change_tag_receive,name='do_tag_receive'),
    path('do_tag_notreceive',views.change_tag_notreceive,name='do_tag_notreceive'),
    path('do_redeliver',views.change_tag_standby,name='do_redeliver'),
    path('do_refund',views.change_tag_refund,name='do_refund'),
    path('update_quantity_value',views.update_quantity_value,name='update_quantity_value'),
    path('update_user_cart', views.update_user_cart, name='update_user_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('Cart',views.Cart_Bag,name='Cart'),
    path('Cashier',views.Cashier,name='Cashier'),
    path('Checkout',views.GotoCheckout,name='Checkout'), #added
    path('HandleCheckout',views.HandleCheckout,name='HandleCheckout'),
    path('FAQs',views.FAQs,name='FAQs'),
    path('FoodDis/<int:FoodId>/', views.FoodDis, name='FoodDis'),
    path('',views.warp,name='warp'),
    path('Home-Page',views.warp,name='warp'),
    path('LogIn',views.LogIn,name='Log-In'),
    path('Menu',views.Menu,name='Menu'),
    path('Profile/',views.Profile,name='Profile'),
    path('Register', views.Register, name='Register'),
    path('SignOut', sign_out, name='SignOut'),
    path('ForgetPass', views.ForgetPass, name='forget_password'), #added
    path('verify-otp/', views.VerifyOTP, name='verify_otp'), #added
    path('TopUp',views.TopUp,name='TopUp'),
    path('topup_to_user',views.topup_apply,name='topup_to_user'),
    path('reset-password/<int:account_id>/', views.ResetPassword, name='reset_password'), #added
    path('full_report_template', views.generate_pdf_view, name='generate_full_report'), #added
    path('generate_report/', views.generate_pdf_view, name='generate_pdf_view'), #added
    path('Done/', views.done_view, name='Done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)