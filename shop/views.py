from lib2to3.fixes.fix_input import context
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, DetailView, ListView
from .models import Review
from django.views.generic import TemplateView
from shop.models import Review
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from shop.models import Product
from shop.services.email import send_email
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from .models import Product

class ProductPageView(TemplateView):
    template_name = 'shop/pages/product.html'

    # Optional: Define context data if needed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context



class ProductListView(ListView):
    model = Product
    template_name = 'shop/pages/product_list.html'
    context_object_name = 'products'
    paginate_by = 12  # Optional: Add pagination


    # Optional: Define context data if needed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100

        return context


class OurCompanyPageView(TemplateView):
    template_name = 'shop/pages/company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100

        return context

class HomePageView(TemplateView):
    template_name = 'shop/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100

        return context


class WhyUsPageView(TemplateView):
    template_name = 'shop/pages/why_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch reviews and calculate percentage for ratings
        reviews = Review.objects.all()
        for review in reviews:
            review.rating_percentage = (review.rating / 5) * 100  # Convert rating to percentage

        context['reviews'] = reviews
        return context


class ContactUsPageView(TemplateView):
    template_name = 'shop/pages/contact_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100


        return context


from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .models import Product

from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Product

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/pages/buy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Calculate the rating as a percentage (rating out of 5 stars)
        rating_percentage = (product.rating / 5) * 100 if product.rating else 0
        context['rating_percentage'] = rating_percentage

        context['flavors'] = product.flavors.all()  # Fetch all related flavors
        return context




class CartPageView(TemplateView):
    template_name = 'shop/pages/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100

        return context

class AuthPageView(TemplateView):
    template_name = 'shop/pages/auth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product_name'] = "Sample Product"
        context['product_price'] = 100

        return context

















