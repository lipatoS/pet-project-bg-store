from django.contrib import admin
from django.urls import path
from store.views import HomeView, CreateProductView, ProductListView, UpdateProductView, DeleteProductView
from store.views import ProductActions
from store.views import UploadExcelView
from store.views import ExportExcelView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home_link'),
    path('products_list', ProductListView.as_view(), name="product_list_link"),
    path('create/', CreateProductView.as_view(), name='product_create_link'),
    path('edit/<int:pk>/', UpdateProductView.as_view(), name='product_edit_link'),
    path('delete/<int:pk>/', DeleteProductView.as_view(), name='product_delete_link'),
    path('actions', ProductActions.as_view(), name='product_actions_link'),
    path('upload/', UploadExcelView.as_view(), name='upload_excel_link'),
    path('export/', ExportExcelView.as_view(), name='export_excel_link'),
]
