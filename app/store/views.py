from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from django.views import View
from .models import Product
from .forms import ProductForm
import pandas as pd
from .forms import UploadFileForm
import io
from rest_framework import generics
from .serializers import ProductSerializer


# Главная страница
class HomeView(TemplateView):
    template_name = "home.html"


# Создать товар
class CreateProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_create.html"
    success_url = reverse_lazy("product_list")


# Просмотр всех товаров
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'


# Обновить информацию о товаре
class UpdateProductView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('product_list_link')


# Удалить товар
class DeleteProductView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list_link')
    template_name = 'product_confirm_delete.html'


# Страница выбора действий добавления или просмотра списка товаров
class ProductActions(TemplateView):
    template_name = "product_actions.html"


class UploadExcelView(View):
    template_name = 'upload.html'
    success_url = reverse_lazy("product_list_link")  # Убедитесь, что у вас есть маршрут с этим именем

    def get(self, request):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                name = row['name']
                price = row['price']
                stock_quantity = row['stock_quantity']

                product = Product.objects.filter(name__iexact=name).first()

                if product:
                    product.price = price
                    product.stock_quantity = stock_quantity
                    product.save()
                else:
                    product = Product(
                        name=name,
                        price=price,
                        stock_quantity=stock_quantity
                    )
                    product.save()

            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class ExportExcelView(View):

    def get(self, request):
        # Получение всех товаров из базы данных
        products = Product.objects.all().values()

        # Преобразование QuerySet в DataFrame
        df = pd.DataFrame.from_records(products)

        # Сохранение DataFrame в байтовый объект
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Products')

        # Получение байтового содержимого Excel-файла
        excel_data = output.getvalue()

        # Создание HTTP-ответа
        response = HttpResponse(excel_data,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'
        return response


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
