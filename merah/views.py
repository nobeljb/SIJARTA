from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime, timedelta
from decimal import Decimal
from utils.query import query

# Dummy data - in real implementation, this would come from SQL server
DUMMY_USER = {
    'phone_number': '081234567890',
    'balance': Decimal('1500000.00'),
    'role': 'Pengguna', # atur rolenya disini
}

DUMMY_TRANSACTIONS = [
    {
        'nominal': Decimal('250000.00'),
        'tanggal': datetime.now() - timedelta(hours=2),
        'kategori': 'Top Up',
    },
    {
        'nominal': Decimal('75000.00'),
        'tanggal': datetime.now() - timedelta(days=1),
        'kategori': 'Payment',
    },
    {
        'nominal': Decimal('100000.00'),
        'tanggal': datetime.now() - timedelta(days=2),
        'kategori': 'Transfer',
    },
    {
        'nominal': Decimal('500000.00'),
        'tanggal': datetime.now() - timedelta(days=3),
        'kategori': 'Top Up',
    },
    {
        'nominal': Decimal('110000.00'),
        'tanggal': datetime.now() - timedelta(days=4),
        'kategori': 'Payment',
    },
    {
        'nominal': Decimal('120000.00'),
        'tanggal': datetime.now() - timedelta(days=4),
        'kategori': 'Payment',
    },
    {
        'nominal': Decimal('60000.00'),
        'tanggal': datetime.now() - timedelta(days=4),
        'kategori': 'Payment',
    },
    {
        'nominal': Decimal('1000.00'),
        'tanggal': datetime.now() - timedelta(days=4),
        'kategori': 'Payment',
    },
    {
        'nominal': Decimal('12000.00'),
        'tanggal': datetime.now() - timedelta(days=4),
        'kategori': 'Payment',
    },
    {
        'nominal': Decimal('1110000.00'),
        'tanggal': datetime.now() - timedelta(days=4),
        'kategori': 'Payment',
    },
    {
        'nominal': Decimal('2222000.00'),
        'tanggal': datetime.now() - timedelta(days=4),
        'kategori': 'Payment',
    },
]

# views.py

DUMMY_JOB_CATEGORIES = [
    'Home Cleaning',
    'Home Cook',
]

DUMMY_SUBCATEGORIES = {
    'Home Cleaning': ['Regular Cleaning', 'Deep Cleaning', 'Window Cleaning'],
    'Personal Driver': ['City Drive', 'Long Distance', 'Airport Transfer'],
    'Home Cook': ['Daily Cooking', 'Event Catering', 'Meal Prep'],
    'Massage': ['Traditional', 'Reflexology', 'Sport Massage'],
}

DUMMY_JOB_ORDERS = [
    {
        'id': 1,
        'kategori': 'Home Cleaning',
        'subkategori': 'Regular Cleaning',
        'status': 'Mencari Pekerja Terdekat',
        'alamat': 'Jl. Kebon Jeruk No. 15',
        'tanggal': '2024-03-20',
        'waktu': '09:00',
        'harga': 'Rp 150.000',
    },
    {
        'id': 2,
        'kategori': 'Home Cleaning',
        'subkategori': 'Deep Cleaning',
        'status': 'Mencari Pekerja Terdekat',
        'alamat': 'Jl. Sudirman No. 100',
        'tanggal': '2024-03-21',
        'waktu': '13:00',
        'harga': 'Rp 300.000',
    },
    {
        'id': 3,
        'kategori': 'Personal Driver',
        'subkategori': 'Airport Transfer',
        'status': 'Mencari Pekerja Terdekat',
        'alamat': 'Jl. Gatot Subroto No. 50',
        'tanggal': '2024-03-22',
        'waktu': '05:00',
        'harga': 'Rp 200.000',
    },

    {
        'id': 4,
        'kategori': 'Personal Cook',
        'subkategori': 'Meal Prep',
        'status': 'Mencari Pekerja Terdekat',
        'alamat': 'Jl. Gatot Subroto No. 50',
        'tanggal': '2024-03-22',
        'waktu': '05:00',
        'harga': 'Rp 200.000',
    },


    {
        'id': 4,
        'kategori': 'Home Cleaning',
        'subkategori': 'Meal Prep',
        'status': 'Menunggu Pekerja Berangkat',
        'alamat': 'Jl. Gatot Subroto No. 50',
        'tanggal': '2024-03-22',
        'waktu': '05:00',
        'harga': 'Rp 200.000',
    },

]

def pekerja_jasa(request):
    """
    View for displaying available job orders for workers
    """
    # Get worker's category (dummy)
    worker_category = ['Home Cleaning', 'Home Cook']
    
    # Filter jobs based on worker's category
    available_jobs = [
    {
        'id': 1,
        'kategori': 'Home Cleaning',
        'subkategori': 'Regular Cleaning',
        'status': 'Mencari Pekerja Terdekat',
        'alamat': 'Jl. Kebon Jeruk No. 15',
        'tanggal': '2024-03-20',
        'waktu': '09:00',
        'harga': 'Rp 150.000',
    },
    {
        'id': 2,
        'kategori': 'Home Cleaning',
        'subkategori': 'Regular Cleaning',
        'status': 'Mencari Pekerja Terdekat',
        'alamat': 'Jl. Sudirman No. 100',
        'tanggal': '2024-03-21',
        'waktu': '13:00',
        'harga': 'Rp 300.000',
    },]
    
    context = {
        'categories': DUMMY_JOB_CATEGORIES,
        'subcategories': DUMMY_SUBCATEGORIES,
        'jobs': available_jobs,
        'worker_category': worker_category,
    }
    return render(request, 'pekerja_jasa.html', context)

def show_mypay(request):
    """
    View for MyPay dashboard displaying user balance and transaction history
    Currently using dummy data, will be replaced with SQL server data later
    """

    penggunalogin = request.session.get('penggunalogin')

    query_str = f""" 
    SELECT * 
    FROM TR_MYPAY TR 
    INNER JOIN KATEGORI_TR_MYPAY K 
    ON TR.kategoriid = K.id_kategori_tr_mypay
    WHERE userid = '{penggunalogin['id_user']}';
    """
    q_transasction = query(query_str)
    paginator = Paginator(q_transasction, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'penggunalogin': penggunalogin,
        'phone_number': penggunalogin['nohp'],
        'balance': penggunalogin['saldomypay'],
        'transactions': page_obj,
        'user_role': penggunalogin['role'],
    }
    return render(request, 'dashboard.html', context)

def transaksi_mypay(request):
    """
    View trcansaction 
    """
    penggunalogin = request.session.get('penggunalogin')

    jasa_query_str = f"""
    SELECT su.nama, tj.totalbiaya
    FROM tr_pemesanan_jasa tj

    INNER JOIN SUBKATEGORI_JASA SU
    ON tj.idkategorijasa = SU.id_subkategori_jasa

    WHERE tj.id_tr_pemesanan_jasa IN (
    SELECT ts.idtrpemesanan
    FROM tr_pemesanan_status ts
    GROUP BY ts.idtrpemesanan
    HAVING COUNT(*) = 1 AND bool_and(ts.idstatus = '40bd17f1-779d-42e7-bcd3-26390d5b251c')
    ) AND 
    tj.idpelanggan = '{penggunalogin['id_user']}'
    ;
    """
    jasa_dipesan = query(jasa_query_str)
    print(jasa_dipesan)

    context = {
        'penggunalogin': penggunalogin,
        'user_role': penggunalogin['role'],
        'list_jasa': jasa_dipesan
    }

    # print(context['user_role'])
    return render(request, 'transaksi_mypay.html', context)


def status_pekerjaan(request):
    """
    View untuk menampilkan dan mengubah status pekerjaan yang sedang dikerjakan oleh pekerja
    """
    status_filter = request.GET.get('status', '')
    nama_filter = request.GET.get('nama', '').lower()

    worker_jobs = [
        job for job in DUMMY_JOB_ORDERS
        if job['status'] in [
            'Menunggu Pekerja Berangkat',
            'Pekerja Tiba Di Lokasi',
            'Pelayanan Jasa Sedang Dilakukan',
            'Pesanan Selesai',
            'Pesanan Dibatalkan',
        ]
    ]

    if status_filter:
        worker_jobs = [job for job in worker_jobs if job['status'] == status_filter]
    if nama_filter:
        worker_jobs = [job for job in worker_jobs if nama_filter in f"{job['kategori']} - {job['subkategori']}".lower()]
    
    context = {
        'jobs': worker_jobs,
    }
    return render(request, 'status_pekerjaan.html', context)

def update_status(request, job_id):
    """
    View untuk mengupdate status pekerjaan via form submission
    """
    if request.method == 'POST':
        new_status = request.POST.get('status')
        for job in DUMMY_JOB_ORDERS:
            if job['id'] == job_id:
                current_status = job['status']
                valid_transitions = {
                    'Menunggu Pekerja Berangkat': 'Pekerja Tiba Di Lokasi',
                    'Pekerja Tiba Di Lokasi': 'Pelayanan Jasa Sedang Dilakukan',
                    'Pelayanan Jasa Sedang Dilakukan': 'Pesanan Selesai',
                }
                if valid_transitions.get(current_status) == new_status:
                    job['status'] = new_status
                    messages.success(request, 'Status pekerjaan berhasil diubah.')
                else:
                    messages.error(request, 'Transisi status tidak valid.')
                break
        else:
            messages.error(request, 'Pekerjaan tidak ditemukan.')
    return redirect('merah:status_pekerjaan')