from skinCare_app.my_views import product_view, genKHQR, order_view, category_view, Payment_view
from django.urls import path

from skinCare_app.my_views.Auth_view import register,login_view, logout_view
from skinCare_app.my_views.CheckOut_view import detail, save_checkout
from skinCare_app.my_views.Payment_view import payment, process_payment, payment_success
from skinCare_app.my_views.Telegram_Notification_view import khqr_payment_callback
from skinCare_app.my_views.body_view import home
from skinCare_app.my_views.cart_view import cart_view, add_to_cart, update_cart_item, remove_cart_item
from skinCare_app.my_views.checkout_view2 import checkout_process
from skinCare_app import views
from skinCare_app.my_views.genKHQR import generate_khqr
from skinCare_app.my_views.order_view import order_list
from skinCare_app.my_views.user_view import user_list, user_delete

urlpatterns = [
    path("", home, name="home"),
    path("api/checkout/", checkout_process),
    path("checkout/", checkout_process, name="checkout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # ----------------------------- Product ---------------------------
    path("products/", product_view.product_list, name="product_list"),
    path("products/create/", product_view.create_product, name="create_product"),
    path("products/edit/<int:product_id>/", product_view.edit_product, name="product_edit"),
    path("products/update/<int:product_id>/", product_view.update_product, name="product_update"),
    path("products/delete/<int:product_id>/", product_view.delete_product, name="product_delete"),

    # ----------------------------- User ---------------------------
    path('admin/users', user_list, name='user_list'),
    path('users/', user_list, name='user_list'),
    path('admin/users/delete/<int:id>', user_delete, name='user_delete'),


# ----------------------------- Login ---------------------------
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

# ----------------------------- Cart ---------------------------
    path("cart/", cart_view, name="cart_view"),
    path("cart/add/", add_to_cart, name="add_to_cart"),
    path("cart/update/", update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", remove_cart_item, name="remove_cart_item"),

# ----------------------------- Personal Detail ---------------------------
    path('detail/', detail, name='detail'),

# ----------------------------- Check Out ---------------------------
    path("checkout/save/", save_checkout, name="save_checkout"),

# ----------------------------- Payment ---------------------------
    path("payment/",payment, name="payment"),
    path("payment/process/", process_payment, name="process_payment"),
    path("payment/success/<int:payment_id>/", payment_success, name="payment_success"),
    path("payments/", Payment_view.payment_list, name="payment_list"),
    path("payments/delete/<int:order_id>/", Payment_view.payment_delete, name="payment_delete"),

# ----------------------------- KHQR ---------------------------
    path('generate-khqr/', generate_khqr, name='generate_khqr'),
    path("khqr-callback/", khqr_payment_callback, name="khqr_callback"),
    path('khqr_status/<int:order_id>/', genKHQR.khqr_status, name='khqr_status'),
    path('check-transaction-status/', genKHQR.check_transaction_status, name='check_transaction_status'),

    # ----------------------------- Order ---------------------------
    path("orders/", order_view.order_list, name="order_list"),
    path("orders/delete/<int:order_id>/", order_view.order_delete, name="order_delete"),

# ====================================== Category ======================================
    path ( "categories/", category_view.category_list, name = "category_list"),
    path ( "categories/create/", category_view.category_create, name = "category_create"),
    path ("categories/edit/<int:category_id>/", category_view.category_edit, name = "category_edit") ,
    path ("categories/delete/<int:category_id>/", category_view.category_delete, name = "category_delete") ,
    path("categories/update/<int:category_id>/", category_view.category_update, name="category_update"),


]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)