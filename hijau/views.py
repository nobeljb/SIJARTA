from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from datetime import datetime
from django import forms
from utils.query import query

DUMMY_USER = {
    'role': 'Pengguna',
}

def homepage(request):

    #query kategori
    query_str = f"""
    select * from kategori_jasa
    """
    categories = query(query_str)

    #query subkategori
    query_str = f"""
    select * from subkategori_jasa
    """
    subcategories = query(query_str)

    #query user

    context={
        'categories': categories,
        'subcategories': subcategories,
        'user_role': DUMMY_USER['role'],
    }
    return render(request, 'homepage.html', context)


from django.shortcuts import render
from django.http import Http404

# Common dummy data
categories = [
    {'id': 1, 'name': 'Kategori Jasa 1', 'subcategories': [
        {'id': 1, 'name': 'Subkategori Jasa 1.1', 'description': 'Deskripsi subkategori 1.1'},
        {'id': 2, 'name': 'Subkategori Jasa 1.2', 'description': 'Deskripsi subkategori 1.2'}
    ]},
    {'id': 2, 'name': 'Kategori Jasa 2', 'subcategories': [
        {'id': 3, 'name': 'Subkategori Jasa 2.1', 'description': 'Deskripsi subkategori 2.1'},
        {'id': 4, 'name': 'Subkategori Jasa 2.2', 'description': 'Deskripsi subkategori 2.2'}
    ]},
    {'id': 3, 'name': 'Kategori Jasa 3', 'subcategories': [
        {'id': 5, 'name': 'Subkategori Jasa 3.1', 'description': 'Deskripsi subkategori 3.1'},
        {'id': 6, 'name': 'Subkategori Jasa 3.2', 'description': 'Deskripsi subkategori 3.2'}
    ]},
]

sessions = [
    {'id': 1, 'name': 'Daily Cleaning', 'price': 100000},
    {'id': 2, 'name': 'Kitchen Cleaning', 'price': 150000},
    {'id': 3, 'name': 'Ironing Service', 'price': 75000}
]

testimonials = [
    {'user_name': 'Sarah', 'date': '2024-11-15', 'text': 'Great service, very professional!', 'worker_name': 'John Doe', 'rating': 5},
    {'user_name': 'Michael', 'date': '2024-11-10', 'text': 'Quick and efficient.', 'worker_name': 'Jane Smith', 'rating': 4},
    {'user_name': 'Emily', 'date': '2024-11-12', 'text': 'Excellent attention to detail.', 'worker_name': 'Alex Johnson', 'rating': 5}
]

workers = [
    {'id': 1, 'name': 'John Doe', 'rating': 4.9, 'finished_jobs': 120, 'phone_number': '081234567890', 
     'birthdate': datetime(1985, 5, 22), 'address': 'Jl. Merdeka No. 10, Jakarta'},
    {'id': 2, 'name': 'Jane Smith', 'rating': 4.7, 'finished_jobs': 85, 'phone_number': '082345678901',
     'birthdate': datetime(1990, 8, 14), 'address': 'Jl. Sudirman No. 15, Bandung'},
    {'id': 3, 'name': 'Alex Johnson', 'rating': 4.8, 'finished_jobs': 102, 'phone_number': '083456789012',
     'birthdate': datetime(1988, 11, 30), 'address': 'Jl. Gatot Subroto No. 25, Yogyakarta'}
]

worker_statuses = [
    {'user_id': 1, 'is_worker': True},
    {'user_id': 2, 'is_worker': False},
    {'user_id': 3, 'is_worker': True}
]

# View for user
def subcategory_detail_user(request, category_id, subcategory_name):
    category = next((cat for cat in categories if cat['id'] == category_id), None)
    if category is None:
        raise Http404("Kategori tidak ditemukan")
    
    subcategory = next((sub for sub in category['subcategories'] if sub['name'].lower() == subcategory_name.lower()), None)
    if subcategory is None:
        raise Http404("Subkategori tidak ditemukan")

    context = {
        'subcategory': subcategory,
        'category_name': category['name'],
        'sessions': sessions,
        'testimonials': testimonials,
        'workers': workers,
        'worker_statuses': worker_statuses,
        'user_role': DUMMY_USER['role']
    }

    return render(request, 'subcategory_user.html', context)

# View for worker
def subcategory_detail_worker(request, category_id, subcategory_name):
    category = next((cat for cat in categories if cat['id'] == category_id), None)
    if category is None:
        raise Http404("Kategori tidak ditemukan")
    
    subcategory = next((sub for sub in category['subcategories'] if sub['name'].lower() == subcategory_name.lower()), None)
    if subcategory is None:
        raise Http404("Subkategori tidak ditemukan")

    context = {
        'subcategory': subcategory,
        'category_name': category['name'],
        'workers': workers,
        'worker_statuses': worker_statuses,
        'sessions': sessions,
        'testimonials': testimonials,
        'user_role': DUMMY_USER['role']
    }

    return render(request, 'subcategory_worker.html', context)

def worker_detail(request, worker_id):
    # Get the worker by ID (or 404 if not found)
    worker = next((w for w in workers if w['id'] == worker_id), None)
    if worker is None:
        raise Http404("Pekerja tidak ditemukan")

    # Pass worker details to the template
    context = {
        'worker': worker,
        'user_role': DUMMY_USER['role']
    }

    return render(request, 'worker_detail.html', context)

# Dummy form untuk pemesanan

class PemesananForm(forms.Form):
    tanggal_pemesanan = forms.DateField(
        widget=forms.SelectDateWidget(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4'
        }),
        initial=forms.fields.DateField,
        label="Tanggal Pemesanan",
    )
    diskon = forms.CharField(
        max_length=100, 
        required=False, 
        label="Diskon (Opsional)",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Masukkan kode diskon jika ada'
        })
    )
    total_pembayaran = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        initial=50000, 
        required=False, 
        label="Total Pembayaran",
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'readonly': 'readonly',
            'value': '50000'
        })
    )
    metode_bayar = forms.ChoiceField(
        choices=[
            ('transfer', 'Transfer Bank'),
            ('credit_card', 'Kartu Kredit'),
            ('e-wallet', 'E-Wallet'),
            ('cash', 'Bayar Tunai')
        ],
        label="Metode Pembayaran",
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
    # Optional: Button style for submit
    submit_button = forms.CharField(widget=forms.HiddenInput(), initial="Submit", required=False)

def create_pemesanan(request):
    if request.method == 'POST':
        form = PemesananForm(request.POST)
        if form.is_valid():
            # Logika untuk menghitung total pembayaran dengan diskon
            diskon_code = form.cleaned_data['diskon']
            total_pembayaran = form.cleaned_data['total_pembayaran']
            if diskon_code == 'PROMO100':
                total_pembayaran -= 10000  # Potongan diskon 10.000

            # Lakukan pengolahan lainnya jika perlu, misalnya menyimpan data ke database
            
            # Redirect ke halaman View Pemesanan Jasa
            return redirect('view_pemesanan')
    else:
        form = PemesananForm()

    return render(request, 'create_pesanan.html', {'form': form, 'user_role': DUMMY_USER['role']})



def view_pemesanan(request):
    # Dummy data pesanan
    pesanan = [
        {
            'session_name': 'Layanan A',
            'session_price': 150000,
            'status': 'menunggu_pembayaran',
            'testimoni': '',
        },
        {
            'session_name': 'Layanan B',
            'session_price': 200000,
            'status': 'mencari_pekerja',
            'testimoni': '',
        },
        {
            'session_name': 'Layanan C',
            'session_price': 250000,
            'status': 'pesanan_selesai',
            'testimoni': '',
        },
        {
            'session_name': 'Layanan D',
            'session_price': 300000,
            'status': 'pesanan_selesai',
            'testimoni': 'Testimoni sudah ada',
        },
    ]
    
    context = {
        'pesanan': pesanan,
        'user_role': DUMMY_USER['role']
    }
    return render(request, 'view_pemesanan.html', context)