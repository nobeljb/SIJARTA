from django.shortcuts import get_object_or_404, render
from django.http import Http404
from datetime import datetime

def homepage(request):
    categories = [
        {"id": 1, "name": "Kategori Jasa 1"},
        {"id": 2, "name": "Kategori Jasa 2"},
        {"id": 3, "name": "Kategori Jasa 3"}
    ]
    
    subcategories = [
        {"category_id": 1, "category_name": "Kategori Jasa 1", "name": "Subkategori Jasa 1.1", "description": "Deskripsi subkategori 1.1"},
        {"category_id": 1, "category_name": "Kategori Jasa 1", "name": "Subkategori Jasa 1.2", "description": "Deskripsi subkategori 1.2"},
        {"category_id": 2, "category_name": "Kategori Jasa 2", "name": "Subkategori Jasa 2.1", "description": "Deskripsi subkategori 2.1"},
        {"category_id": 2, "category_name": "Kategori Jasa 2", "name": "Subkategori Jasa 2.2", "description": "Deskripsi subkategori 2.2"},
        {"category_id": 3, "category_name": "Kategori Jasa 3", "name": "Subkategori Jasa 3.1", "description": "Deskripsi subkategori 3.1"},
        {"category_id": 3, "category_name": "Kategori Jasa 3", "name": "Subkategori Jasa 3.2", "description": "Deskripsi subkategori 3.2"},
    ]

    return render(request, 'index.html', {'categories': categories, 'subcategories': subcategories})


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
        'worker_statuses': worker_statuses
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
        'testimonials': testimonials
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
    }

    return render(request, 'worker_detail.html', context)