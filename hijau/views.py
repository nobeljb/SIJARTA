from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse, JsonResponse
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

    #pengguna lagoin
    penggunalogin = request.session.get('penggunalogin')

    context={
        'categories': categories,
        'subcategories': subcategories,
        'penggunalogin': penggunalogin,
    }
    return render(request, 'homepage.html', context)

# View for user
def subcategory_detail(request, category_id, subcategory_nama):
    penggunalogin = request.session.get('penggunalogin')

    #query kategori
    query_str = f"""
    select * from kategori_jasa
    where id_kategori_jasa = '{category_id}'
    """
    categories = query(query_str)

    #query subkategori
    query_str = f"""
    select * from subkategori_jasa
    where nama = '{subcategory_nama}'
    """
    subcategories = query(query_str)

    #query sesi_layanan
    query_str = f"""
    select * from sesi_layanan
    where id_subkategori = '{subcategories[0]['id_subkategori_jasa']}'
    """
    sessions = query(query_str)

    #query testimoni
    query_str = f"""
    select pgn1.nama as namapengguna, pgn2.nama as namapekerja, tst.tgl as tanggal, tst.teks, tst.rating
    from tr_pemesanan_jasa tpj
    join pengguna pgn1 on tpj.idpelanggan = pgn1.id_user
    join pengguna pgn2 on tpj.idpekerja = pgn2.id_user
    join testimoni tst on tpj.id_tr_pemesanan_jasa = tst.idtrpemesanan
    where tpj.idkategorijasa = '{subcategories[0]['id_subkategori_jasa']}';
    """
    testimonials = query(query_str)

    #query testimoni
    query_str = f"""
    select pgn.nama
    from sijarta.pekerja_kategori_jasa pkj
    join sijarta.pengguna pgn on pgn.id_user = pkj.pekerjaid
    where pkj.kategorijasaid ='{categories[0]['id_kategori_jasa']}';
    """
    workers = query(query_str)
    
    joined = False

    for worker in workers:
        if(worker['nama'] == penggunalogin['nama']):
            joined = True

    context={
        'category_name': categories[0]['namakategori'],
        'subcategory': subcategories[0],
        'penggunalogin': penggunalogin,
        'sessions': sessions,
        'testimonials': testimonials,
        'workers': workers,
        'joined': joined,
    }

    if(penggunalogin.get('role') == 'pengguna'):
        return render(request, 'subcategory_user.html', context)
    else:
        return render(request, 'subcategory_worker.html', context)

def join_subcategory(request, subcategory_id, pekerja_id):
    penggunalogin = request.session.get('penggunalogin')
    #query subkategori
    query_str = f"""
    select * from subkategori_jasa
    where id_subkategori_jasa = '{subcategory_id}'
    """
    subcategories = query(query_str)

    query_str = f"""
    insert into pekerja_kategori_jasa values(
    '{pekerja_id}', '{subcategories[0]['kategorijasaid']}')
    """
    hasil = query(query_str)
    
    # Respons JSON
    try:
        # Operasi sukses
        return JsonResponse({
            'status': 'success',
            'message': f'Berhasil bergabung',
            'pekerja_nama': penggunalogin['nama'],  # Gantilah ini sesuai dengan data yang benar
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
        })
    
# Common dummy data

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