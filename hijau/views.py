import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse, JsonResponse
from datetime import date, datetime
from django import forms
from utils.query import query
from urllib.parse import unquote

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

    # Ubah %20 menjadi spasi
    subcategory_nama = unquote(subcategory_nama)
    
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
    from pekerja_kategori_jasa pkj
    join pengguna pgn on pgn.id_user = pkj.pekerjaid
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

def worker_detail(request, worker_name):
    penggunalogin = request.session.get('penggunalogin')

    worker_name = unquote(worker_name)

    query_str = f"""
    select * from pengguna
    join pekerja on id_user = id_pekerja
    where nama = '{worker_name}'
    """
    pekerja = query(query_str)

    context = {
        'pekerja': pekerja[0],
        'penggunalogin': penggunalogin,
    }
    
    return render(request, "worker_detail.html", context)
class PemesananForm(forms.Form):
    query_str = f"""
    select * from metode_bayar
    """
    metode_pembayaran = query(query_str)

    diskon = forms.CharField(
        max_length=100, 
        required=False, 
        label="Diskon (Opsional)",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2C5F59]',
            'placeholder': 'Masukkan kode diskon jika ada'
        })
    )
    metode_bayar = forms.ChoiceField(
        choices=[(metode['id_metode_bayar'], metode['nama']) for metode in metode_pembayaran],
        label="Metode Pembayaran",
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2C5F59]'
        })
    )
    
    # Optional: Button style for submit
    submit_button = forms.CharField(widget=forms.HiddenInput(), initial="Submit", required=False)

def create_pemesanan(request, subcategory_id, session, price):
    penggunalogin = request.session.get('penggunalogin')
    tanggal_pemesanan = date.today()
    context = {
        'tanggal_pemesanan': tanggal_pemesanan,
        'harga': price,
        'penggunalogin': penggunalogin,
    }
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = PemesananForm(request.POST)
        if form.is_valid():
            # Ambil data dari form
            diskon_code = form.cleaned_data.get('diskon', '')  # Default '' jika kosong
            metode_bayar = form.cleaned_data['metode_bayar']
            harga_akhir = float(price)  # Default harga adalah harga awal
            berhasil_diskon = False

            # Cek apakah kode promo valid terlebih dahulu
            if diskon_code:
                query_str = f"""
                    SELECT * FROM promo
                    JOIN diskon ON kode_diskon = kode_promo
                    WHERE kode_promo = '{diskon_code}' AND tglakhirberlaku >= current_date
                """
                promo_data = query(query_str)

                if promo_data:
                    promo = promo_data[0]
                    min_transaksi = float(promo['mintrpemesanan'])
                    potongan = float(promo['potongan'])
                    berhasil_diskon = True

                    if float(price) < min_transaksi:
                        # Promo tidak valid (harga kurang dari min_transaksi)
                        return JsonResponse({'success': False, 'message': 'Harga tidak memenuhi syarat minimum transaksi.'})
                    else:
                        harga_akhir -= potongan

                else:
                    # Jika promo tidak ditemukan, cek apakah kode diskon valid
                    query_diskon = f"""
                    SELECT * FROM tr_pembelian_voucher
                    JOIN diskon ON kode_diskon = idvoucher
                    JOIN voucher ON kode_voucher = idvoucher
                    WHERE idpelanggan = '{penggunalogin['id_user']}' AND idvoucher = '{diskon_code}' AND tglakhir >= current_date AND tglawal <= current_date AND telahdigunakan < kuotapenggunaan
                    ORDER BY tglawal ASC, tglakhir ASC
                    """
                    diskon_data = query(query_diskon)

                    if diskon_data:
                        diskon = diskon_data[0]  # Ambil data diskon pertama (jika ada)
                        min_transaksi = float(diskon['mintrpemesanan'])
                        potongan = float(diskon['potongan'])
                        berhasil_diskon = True

                        if float(price) < min_transaksi:
                            # Diskon tidak valid (harga kurang dari min_transaksi)
                            return JsonResponse({'success': False, 'message': 'Harga tidak memenuhi syarat minimum transaksi.'})
                        else:
                            harga_akhir -= potongan  # Kurangi harga dengan potongan
                            query_str = f"""
                            UPDATE tr_pembelian_voucher 
                            SET telahdigunakan = telahdigunakan + 1
                            WHERE id_tr_pembelian_voucher = '{diskon['id_tr_pembelian_voucher']}'
                            """
                            query(query_str)
                    else:
                        # Jika kode diskon juga tidak valid
                        return JsonResponse({'success': False, 'message': 'Kode diskon/promo tidak valid.'})

            id_pemesanan = uuid.uuid4()
            # Simpan pemesanan ke database
            if(berhasil_diskon):
                query_str = f"""
                INSERT INTO tr_pemesanan_jasa 
                (idkategorijasa, idpelanggan, id_tr_pemesanan_jasa, totalbiaya, tglpemesanan, idmetodebayar, sesi, iddiskon) 
                VALUES 
                ('{subcategory_id}', '{penggunalogin['id_user']}', '{id_pemesanan}', '{harga_akhir}', current_date, '{metode_bayar}', '{session}', '{diskon_code}')
                """
            else:
                query_str = f"""
                INSERT INTO tr_pemesanan_jasa 
                (idkategorijasa, idpelanggan, id_tr_pemesanan_jasa, totalbiaya, tglpemesanan, idmetodebayar, sesi, iddiskon) 
                VALUES 
                ('{subcategory_id}', '{penggunalogin['id_user']}', '{id_pemesanan}', '{harga_akhir}', current_date, '{metode_bayar}', '{session}', null)
                """
            
            query(query_str)

            if metode_bayar == 'ab9aab5e-5706-4c35-8099-765b7f41a925':
                query_str = f"""
                    insert into tr_pemesanan_status values('{id_pemesanan}', '40bd17f1-779d-42e7-bcd3-26390d5b251c', current_date)
                    """
            else:
                query_str = f"""
                    insert into tr_pemesanan_status values('{id_pemesanan}', '2dd8907b-bb4e-4dd2-a6ce-613a63255391', current_date)
                    """
            query(query_str)

            return JsonResponse({'success': True, 'message': 'Pemesanan berhasil dibuat.'})

    else:  # GET request, tampilkan form kosong
        context['form'] = PemesananForm()

    return render(request, 'create_pesanan.html', context)
    
def view_pemesanan(request):
    penggunalogin = request.session.get('penggunalogin')
    query_str = f"""
    SELECT DISTINCT ON (pj.id_tr_pemesanan_jasa) 
        pj.id_tr_pemesanan_jasa AS id_pemesanan,
        sj.deskripsi AS session_name, 
        pj.totalbiaya AS session_price,
        pg.nama AS worker_name,
        sp.status,
        ps.tglwaktu
    FROM sijarta.tr_pemesanan_jasa pj
    JOIN sijarta.tr_pemesanan_status ps 
        ON pj.id_tr_pemesanan_jasa = ps.idtrpemesanan
    JOIN sijarta.subkategori_jasa sj 
        ON sj.id_subkategori_jasa = pj.idkategorijasa
    JOIN sijarta.status_pesanan sp 
        ON sp.id_status_pesanan = ps.idstatus
    LEFT JOIN sijarta.pengguna pg
        ON pg.id_user = pj.idpekerja
    WHERE pj.idpelanggan = '{penggunalogin['id_user']}'
    ORDER BY 
        pj.id_tr_pemesanan_jasa,  -- Mengelompokkan per pesanan
        ps.tglwaktu DESC,         -- Ambil status terbaru berdasarkan waktu
        CASE 
            WHEN sp.status = 'Pesanan dibatalkan' THEN 1
            WHEN sp.status = 'Pesanan selesai' THEN 2
            WHEN sp.status = 'Pelayanan jasa sedang dilakukan' THEN 3
            WHEN sp.status = 'Pekerja tiba di lokasi' THEN 4
            WHEN sp.status = 'Menunggu Pekerja Berangkat' THEN 5
            WHEN sp.status = 'Mencari Pekerja Terdekat' THEN 6
            WHEN sp.status = 'Menunggu Pembayaran' THEN 7
            ELSE 8 -- Default jika status tidak dikenal
        END;
    """
    pesanan = query(query_str)
    if pesanan:
        for pesan in pesanan:
            query_str = f"""
            SELECT * FROM testimoni
            WHERE idtrpemesanan = '{pesan['id_pemesanan']}'
            """
            testimoni = query(query_str)
            pesan['testimoni'] = testimoni[0]['teks'] if testimoni else ''
    
    context = {
        'pesanan': pesanan,
        'penggunalogin': penggunalogin,
    }
    return render(request, 'view_pemesanan.html', context)

def batal_pemesanan(request, id_pemesanan):
    query_str = f"""
    insert into tr_pemesanan_status values('{id_pemesanan}', '506bb50a-5943-4eb7-a48c-00334aeba847', current_date)
    """
    query(query_str)
    
    penggunalogin = request.session.get('penggunalogin')

    query_str = f"""
    select saldomypay from pengguna
    where id_user = '{penggunalogin['id_user']}'
    """
    pengguna = query(query_str)

    penggunalogin['saldomypay'] = str(pengguna[0]['saldomypay'])
    request.session['penggunalogin'] = penggunalogin
    
    return redirect('hijau:view_pemesanan')