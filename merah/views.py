import json
import uuid
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

# views.py

def pekerja_jasa(request):
    """View for workers to see and accept available jobs"""
    penggunalogin = request.session.get('penggunalogin')
    
    if not penggunalogin or penggunalogin.get('role') != 'pekerja':
        messages.error(request, 'Anda harus login sebagai pekerja')
        return redirect('merah:login')

    query_str = f"""
    SELECT kj.id_kategori_jasa, kj.namakategori 
    FROM KATEGORI_JASA kj
    INNER JOIN PEKERJA_KATEGORI_JASA pkj 
    ON kj.id_kategori_jasa = pkj.kategorijasaid
    WHERE pkj.pekerjaid = '{penggunalogin['id_user']}'
    """
    categories = query(query_str)

    # Get filter parameters
    category_filter = request.GET.get('category', '')
    subcategory_filter = request.GET.get('subcategory', '')

    # Get subcategories for the worker's categories
    query_str = f"""
    SELECT sj.id_subkategori_jasa, sj.nama, sj.kategorijasaid
    FROM SUBKATEGORI_JASA sj
    INNER JOIN KATEGORI_JASA kj ON sj.kategorijasaid = kj.id_kategori_jasa
    WHERE kj.id_kategori_jasa IN (
        SELECT kategorijasaid FROM PEKERJA_KATEGORI_JASA 
        WHERE pekerjaid = '{penggunalogin['id_user']}'
    )
    """
    subcategories = query(query_str)

    # Modified query to get available jobs
    base_query = f"""
    SELECT 
        tj.id_tr_pemesanan_jasa,
        kj.namakategori as kategori,
        sj.nama as subkategori,
        tj.tglpemesanan,
        tj.totalbiaya,
        p.alamat,
        sl.sesi,
        sp.status as status_pesanan
    FROM TR_PEMESANAN_JASA tj
    INNER JOIN SUBKATEGORI_JASA sj ON tj.idkategorijasa = sj.id_subkategori_jasa
    INNER JOIN KATEGORI_JASA kj ON sj.kategorijasaid = kj.id_kategori_jasa
    INNER JOIN PENGGUNA p ON tj.idpelanggan = p.id_user
    INNER JOIN SESI_LAYANAN sl ON tj.idkategorijasa = sl.id_subkategori AND tj.sesi = sl.sesi
    INNER JOIN (
        SELECT idtrpemesanan, idstatus
        FROM tr_pemesanan_status
        WHERE (idtrpemesanan, tglwaktu) IN (
            SELECT idtrpemesanan, MAX(tglwaktu)
            FROM tr_pemesanan_status
            GROUP BY idtrpemesanan
        )
    ) ts ON tj.id_tr_pemesanan_jasa = ts.idtrpemesanan
    INNER JOIN STATUS_PESANAN sp ON ts.idstatus = sp.id_status_pesanan
    WHERE tj.idpekerja IS NULL
    AND sp.id_status_pesanan = '2dd8907b-bb4e-4dd2-a6ce-613a63255391'
    AND kj.id_kategori_jasa IN (
        SELECT kategorijasaid FROM PEKERJA_KATEGORI_JASA 
        WHERE pekerjaid = '{penggunalogin['id_user']}'
    )
    """

    # Apply filters if selected
    if category_filter:
        base_query += f" AND kj.id_kategori_jasa = '{category_filter}'"
    if subcategory_filter:
        base_query += f" AND sj.id_subkategori_jasa = '{subcategory_filter}'"

    jobs = query(base_query)

    # Handle job acceptance
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            # Insert new status
            status_query = f"""
            INSERT INTO TR_PEMESANAN_STATUS (idtrpemesanan, idstatus, tglwaktu)
            VALUES ('{job_id}', 'ff584044-c977-4424-a57a-c2db0eb360b8', NOW())
            """
            query(status_query)

            # Update job with worker info and dates
            update_query = f"""
            UPDATE TR_PEMESANAN_JASA
            SET idpekerja = '{penggunalogin['id_user']}',
                tglpekerjaan = CURRENT_DATE,
                waktupekerjaan = CURRENT_DATE + interval '1 day' * sesi
            WHERE id_tr_pemesanan_jasa = '{job_id}'
            """
            query(update_query)
            
            messages.success(request, 'Pesanan berhasil diambil')
            return redirect('merah:pekerja_jasa')

    context = {
        'penggunalogin': penggunalogin,
        'categories': categories,
        'subcategories': subcategories,
        'jobs': jobs,
        'selected_category': category_filter,
        'selected_subcategory': subcategory_filter
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

    query_str = f"""
    select saldomypay from pengguna
    where id_user = '{penggunalogin['id_user']}'
    """
    pengguna = query(query_str)
    penggunalogin['saldomypay'] = str(pengguna[0]['saldomypay'])
    request.session['penggunalogin'] = penggunalogin

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

    print(f"Request method: {request.method}")
    penggunalogin = request.session.get('penggunalogin')
    if not penggunalogin:
        return redirect('merah:login')

    if request.method == 'POST':
            print("aaa")
            print("POST data:", request.POST)
            selected_state = request.POST.get('selectedState')
            print(f"sitolol ini: {selected_state}")
            id_tr = uuid.uuid4()

            if selected_state == 'Payment':
                print("masuk")
                jasa = request.POST.get('jasa')
                print(jasa)
                nominal_payment = request.POST.get('nominal_payment')

                # Validasi input jasa dan nominal_payment
                if not jasa or not nominal_payment:
                    messages.error(request, 'Jasa dan nominal pembayaran harus diisi.')
                    return redirect('transaksi_mypay')

                try:
                    nominal_payment = Decimal(nominal_payment)
                    if nominal_payment <= 0:
                        raise ValueError
                except:
                    messages.error(request, 'Nominal pembayaran tidak valid.')
                    return redirect('transaksi_mypay')

                user_id = penggunalogin['id_user']
                query_str = f"""
                INSERT INTO TR_MYPAY (id_tr_mypay, userid, tgl, nominal, kategoriid)
                VALUES ('{id_tr}', '{user_id}' , NOW(), {nominal_payment}, 'aeb1ae67-aac9-4ef3-8473-a04b33458551');
                """
                hasil_add = query(query_str)

                query_str = f"""
                    UPDATE PENGGUNA
                    SET saldomypay = saldomypay - {nominal_payment}
                    WHERE id_user = '{user_id}';
                    """
                hasil_update = query(query_str)

                query_str = f"""
                SELECT saldomypay FROM pengguna
                where id_user = '{user_id}'
                """
                update_saldo = query(query_str)
                request.session['penggunalogin']['saldomypay'] = update_saldo[0]['saldomypay']

                messages.success(request, f'Pembayaran sebesar Rp {nominal_payment:,.2f} berhasil.')
 
                query_str = f"""
                INSERT INTO TR_PEMESANAN_STATUS (idtrpemesanan, idstatus, tglwaktu)
                VALUES ('{jasa}', '2dd8907b-bb4e-4dd2-a6ce-613a63255391', NOW());
                """
                hasil_status = query(query_str)

                # return redirect('merah:transaksi_mypay')

            elif selected_state == 'TopUp':
                nominal_topup = request.POST.get('nominal_topup')

                # Validasi input nominal_topup
                if not nominal_topup:
                    messages.error(request, 'Nominal top up harus diisi.')
                    return redirect('transaksi_mypay')

                try:
                    nominal_topup = Decimal(nominal_topup)
                    if nominal_topup <= 0:
                        raise ValueError
                except:
                    messages.error(request, 'Nominal top up tidak valid.')
                    return redirect('transaksi_mypay')
                
                user_id = penggunalogin['id_user']
                query_str = f"""
                INSERT INTO TR_MYPAY (id_tr_mypay, userid, tgl, nominal, kategoriid)
                VALUES ('{id_tr}', '{user_id}' , NOW(), {nominal_topup}, '637a8319-3473-46fc-b907-c4271dd098a6');
                """
                hasil_add = query(query_str)

                query_str = f"""
                    UPDATE PENGGUNA
                    SET saldomypay = saldomypay + {nominal_topup}
                    WHERE id_user = '{user_id}';
                    """
                hasil_update = query(query_str)

                query_str = f"""
                    SELECT saldomypay FROM pengguna
                    where id_user = '{user_id}'
                    """
                update_saldo = query(query_str)
                print(update_saldo)
                penggunalogin['saldomypay'] = update_saldo[0]['saldomypay']

                # return redirect('merah:transaksi_mypay')

            elif selected_state == 'Transfer':
                no_hp_tujuan = request.POST.get('no_hp_tujuan')
                nominal_transfer = request.POST.get('nominal_transfer')

                if not no_hp_tujuan or not nominal_transfer:
                    messages.error(request, 'Nomor HP tujuan dan nominal transfer harus diisi.')
                    return redirect('merah:transaksi_mypay')

                try:
                    nominal_transfer = Decimal(nominal_transfer)
                    if nominal_transfer <= 0:
                        raise ValueError
                except:
                    messages.error(request, 'Nominal transfer tidak valid.')
                    return redirect('merah:transaksi_mypay')

                # Check if sender has sufficient balance
                current_balance = Decimal(str(penggunalogin['saldomypay']))
                if current_balance < nominal_transfer:
                    messages.error(request, 'Saldo tidak mencukupi untuk melakukan transfer.')
                    return redirect('merah:transaksi_mypay')

                # Check if recipient exists
                query_str = f"""
                SELECT id_user, saldomypay FROM pengguna WHERE nohp = '{no_hp_tujuan}'
                """
                recipient = query(query_str)

                if not recipient:
                    messages.error(request, 'Nomor HP tujuan tidak ditemukan.')
                    return redirect('merah:transaksi_mypay')

                recipient_id = recipient[0]['id_user']

                transfer_out_id = uuid.uuid4()
                transfer_in_id = uuid.uuid4()

                query_str = f"""
                INSERT INTO TR_MYPAY (id_tr_mypay, userid, tgl, nominal, kategoriid)
                VALUES ('{transfer_out_id}', '{penggunalogin['id_user']}', NOW(), {nominal_transfer}, '43de9edc-bee8-417d-bf1a-e135cd8006f1');
                """
                query(query_str)

                # Create transfer in transaction
                query_str = f"""
                INSERT INTO TR_MYPAY (id_tr_mypay, userid, tgl, nominal, kategoriid)
                VALUES ('{transfer_in_id}', '{recipient_id}', NOW(), {nominal_transfer}, '43de9edc-bee8-417d-bf1a-e135cd8006f1');
                """
                query(query_str)

                # Update sender balance
                query_str = f"""
                UPDATE PENGGUNA 
                SET saldomypay = saldomypay - {nominal_transfer}
                WHERE id_user = '{penggunalogin['id_user']}';
                """
                query(query_str)

                # Update recipient balance
                query_str = f"""
                UPDATE PENGGUNA 
                SET saldomypay = saldomypay + {nominal_transfer}
                WHERE id_user = '{recipient_id}';
                """
                query(query_str)

                # Update session balance
                query_str = f"""
                SELECT saldomypay FROM pengguna WHERE id_user = '{penggunalogin['id_user']}'
                """
                update_saldo = query(query_str)
                penggunalogin['saldomypay'] = update_saldo[0]['saldomypay']

                messages.success(request, f'Transfer sebesar Rp {nominal_transfer:,.2f} ke {no_hp_tujuan} berhasil.')

            elif selected_state == "Withdrawal":
                nominal_withdrawal = request.POST.get('nominal_withdrawal')
                user_id = penggunalogin['id_user']

                query_str = f"""
                INSERT INTO TR_MYPAY(id_tr_mypay, userid, tgl, nominal, kategoriid)
                VALUES ('{id_tr}', '{user_id}', NOW(), {nominal_withdrawal}, '79f60eae-c677-4b08-80ae-4c0adc361317');
                """

                hasil_add = query(query_str)

                query_str = f"""
                UPDATE PENGGUNA
                SET saldomypay = saldomypay - {nominal_withdrawal}
                WHERE id_user = '{user_id}';
                """
                hasil_update = query(query_str)

                query_str = f"""
                SELECT saldomypay FROM pengguna WHERE id_user = '{user_id}'
                """
                update_saldo = query(query_str)
                request.session['penggunalogin']['saldomypay'] = str(update_saldo[0]['saldomypay'])


    jasa_query_str = f"""
        SELECT su.nama, tj.totalbiaya, tj.id_tr_pemesanan_jasa
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

    context = {
        'penggunalogin': penggunalogin,
        'user_role': penggunalogin['role'],
        'list_jasa': jasa_dipesan
    }

    # print(context['user_role'])
    return render(request, 'transaksi_mypay.html', context)


def status_pekerjaan(request):
    penggunalogin = request.session.get('penggunalogin')
    
    if not penggunalogin or penggunalogin.get('role') != 'pekerja':
        messages.error(request, 'Anda harus login sebagai pekerja')
        return redirect('merah:login')

    status_filter = request.GET.get('status', '')
    nama_filter = request.GET.get('nama', '').lower()

    # Modified query to only show accepted jobs
    base_query = f"""
    SELECT DISTINCT ON (pj.id_tr_pemesanan_jasa)
        pj.id_tr_pemesanan_jasa,
        kj.namakategori as kategori,
        sj.nama as subkategori,
        pj.tglpemesanan,
        pj.totalbiaya,
        p.alamat,
        sp.status as current_status,
        sp.id_status_pesanan as status_id,
        ts.tglwaktu
    FROM TR_PEMESANAN_JASA pj
    INNER JOIN SUBKATEGORI_JASA sj ON pj.idkategorijasa = sj.id_subkategori_jasa
    INNER JOIN KATEGORI_JASA kj ON sj.kategorijasaid = kj.id_kategori_jasa
    INNER JOIN PENGGUNA p ON pj.idpelanggan = p.id_user
    INNER JOIN (
        SELECT idtrpemesanan, idstatus, tglwaktu
        FROM tr_pemesanan_status
        WHERE (idtrpemesanan, tglwaktu) IN (
            SELECT idtrpemesanan, MAX(tglwaktu)
            FROM tr_pemesanan_status
            GROUP BY idtrpemesanan
        )
    ) ts ON pj.id_tr_pemesanan_jasa = ts.idtrpemesanan
    INNER JOIN STATUS_PESANAN sp ON ts.idstatus = sp.id_status_pesanan
    WHERE pj.idpekerja = '{penggunalogin['id_user']}'
    AND sp.id_status_pesanan IN (
        'ff584044-c977-4424-a57a-c2db0eb360b8',  -- Menunggu Pekerja Berangkat
        '230342c4-f48c-40f9-ae02-bd9b36939316',  -- Pekerja Tiba Di Lokasi
        '3ff38f75-44d4-4926-b050-d6086730e1e6',  -- Pelayanan Jasa Sedang Dilakukan
        '578d6271-7af3-4097-b139-5f1ffbae80f1'   -- Pesanan Selesai
    )
    """

    if nama_filter:
        base_query += f" AND (LOWER(kj.namakategori) LIKE '%{nama_filter}%' OR LOWER(sj.nama) LIKE '%{nama_filter}%')"
        base_query += """
        ORDER BY pj.id_tr_pemesanan_jasa, ts.tglwaktu DESC;
        """

    jobs = query(base_query)

    if status_filter:
        jobs = [job for job in jobs if job['current_status'] == status_filter]

    # Handle status updates
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        new_status = request.POST.get('status')
        
        if job_id and new_status:
            status_mapping = {
                'Pekerja tiba di lokasi': '230342c4-f48c-40f9-ae02-bd9b36939316',
                'Pelayanan jasa sedang dilakukan': '3ff38f75-44d4-4926-b050-d6086730e1e6',
                'Pesanan selesai': '578d6271-7af3-4097-b139-5f1ffbae80f1'
            }
            
            status_id = status_mapping.get(new_status)
            print(f"Jb Id: {job_id}")
            print(f"statustsututus: {status_id}")
            if status_id:
                query_str = f"""
                INSERT INTO TR_PEMESANAN_STATUS (idtrpemesanan, idstatus, tglwaktu)
                VALUES ('{job_id}', '{status_id}', NOW());
                """
                query(query_str)
                return redirect('merah:status_pekerjaan')

    context = {
        'penggunalogin': penggunalogin,
        'jobs': jobs,
        'selected_status': status_filter
    }

    return render(request, 'status_pekerjaan.html', context)