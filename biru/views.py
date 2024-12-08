from django.shortcuts import render, redirect
from django.http import Http404,  JsonResponse
from django.urls import reverse
from utils.query import query
from datetime import datetime, timedelta
import uuid

def testimoni_form(request, id_pemesanan):  # Add id_pemesanan as a parameter
    if request.method == "POST":
        # Get the order ID from the URL parameter
        idtrpemesanan = id_pemesanan
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")
        
        # Insert the new testimony into the database
        query_str = f"""
        INSERT INTO testimoni (idtrpemesanan, tgl, teks, rating)
        VALUES ('{idtrpemesanan}', '{datetime.today().strftime('%Y-%m-%d')}', '{comment}', {rating});
        """
        query(query_str)
        
        # Update the order to mark testimony as submitted
        # update_query = f"""
        # UPDATE transaksi_pemesanan 
        # SET testimoni = 'submitted' 
        # WHERE id_pemesanan = '{id_pemesanan}';
        # """
        # query(update_query)

        query_layanan = f"""
        SELECT sk.nama
        FROM subkategori_jasa sk
        JOIN tr_pemesanan_jasa tpj ON sk.id_subkategori_jasa = tpj.idkategorijasa
        WHERE tpj.id_tr_pemesanan_jasa = '{idtrpemesanan}';
        """
        layanan = query(query_layanan)

        query_kategori = f"""
        SELECT sk.kategorijasaid
        FROM subkategori_jasa sk
        JOIN tr_pemesanan_jasa tpj ON sk.id_subkategori_jasa = tpj.idkategorijasa
        WHERE tpj.id_tr_pemesanan_jasa = '{idtrpemesanan}';
        """
        kategori = query(query_kategori)
        
        # Extract the actual values from the query results
        if kategori and layanan:
            # Assuming each query result contains a single row with one column
            kategori_value = kategori[0]['kategorijasaid']  # Extract UUID value
            layanan_value = layanan[0]['nama']  # Extract name of the service

            # Construct the URL dynamically
            url = reverse('hijau:subcategory_detail_user', args=[kategori_value, layanan_value])

            # Redirect to the dynamically constructed URL
            return redirect(url)
    
    return render(request, "testimoni_form.html", {'id_pemesanan': id_pemesanan})


# Placeholder for testimonies
testimonies = [
    {
        "user_name": "John Doe",
        "date": "2024-11-15",
        "testimony_text": "This is a great service!",
        "worker_name": "Jane Smith",
        "rating": 5,
    },
    # Add more testimonies if needed
]

# View for Testimony Cards
def testimoni_cards(request):
    # Retrieve testimonies from the database
    query_str = """
    SELECT t.idtrpemesanan, t.tgl, t.teks, t.rating, 
           p.nama_pekerja AS worker_name, 
           tpj.tglpekerjaan
    FROM testimoni t
    JOIN tr_pemesanan_jasa tpj ON t.idtrpemesanan = tpj.id_tr_pemesanan_jasa
    JOIN pekerja p ON tpj.idpekerja = p.id_pekerja
    ORDER BY t.tgl DESC;
    """
    testimonies = query(query_str)

    return render(request, "testimoni_cards.html", {"testimonies": testimonies})


# View for Discounts and Promotions
def diskon(request):
    # Retrieve voucher data
    query_str_vouchers = """
    SELECT kode_voucher AS code, jmlhariberlaku AS remaining_days, 
           kuotapenggunaan AS quota, harga AS price
    FROM voucher
    WHERE jmlhariberlaku > 0;  -- Only fetch valid vouchers
    """
    vouchers = query(query_str_vouchers)

    # Retrieve promo data
    query_str_promos = """
    SELECT kode_promo AS code, tglakhirberlaku AS end_date
    FROM promo
    WHERE tglakhirberlaku >= CURRENT_DATE;  -- Only fetch active promos
    """
    promos = query(query_str_promos)

    return render(request, "diskon.html", {"vouchers": vouchers, "promos": promos})


def pembelian_voucher(request):
    try:
        # Get logged-in user from session
        pelanggan = request.session.get('penggunalogin')
        if not pelanggan:
            return JsonResponse({'status': 'failure', 'message': 'Pengguna tidak login.'})
        
        idpelanggan = pelanggan['id_user']
        balance = float(pelanggan['saldomypay'])
        
        # Get voucher code from POST data
        voucher_code = request.POST.get('voucher_code')
        
        # Fetch voucher details
        query_voucher = f"""
        SELECT harga AS price, jmlhariberlaku AS duration, kuotapenggunaan AS quota
        FROM voucher
        WHERE kode_voucher = '{voucher_code}';
        """
        voucher_data = query(query_voucher)
        if not voucher_data:
            return JsonResponse({'status': 'failure', 'message': 'Voucher tidak ditemukan.'})
        
        price = float(voucher_data[0]["price"])
        duration = int(voucher_data[0]["duration"])
        quota = voucher_data[0]["quota"]
        
        # Check balance
        if balance < price:
            return JsonResponse({'status': 'failure', 'message': 'Saldo tidak mencukupi.'})
        
        # Deduct balance and update
        new_balance = balance - price
        update_balance_query = f"""
        UPDATE pengguna
        SET saldomypay = {new_balance}
        WHERE id_user = '{idpelanggan}';
        """
        query(update_balance_query)
        
        # Update session balance
        pelanggan['saldomypay'] = new_balance
        request.session['penggunalogin'] = pelanggan
        request.session.modified = True
        
        # Insert voucher purchase record
        id_tr_pembelian_voucher = str(uuid.uuid4())
        today = datetime.today().date()
        end_date = today + timedelta(days=duration)
        insert_purchase_query = f"""
        INSERT INTO tr_pembelian_voucher (
            id_tr_pembelian_voucher, tglawal, tglakhir, telahdigunakan,
            idpelanggan, idvoucher, idmetodebayar
        ) VALUES (
            '{id_tr_pembelian_voucher}', '{today}', '{end_date}', 0,
            '{idpelanggan}', '{voucher_code}', NULL
        );
        """
        query(insert_purchase_query)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Berhasil membeli voucher {voucher_code}',
            'new_balance': new_balance,
            'end_date': str(end_date),
            'quota': quota  # Ensure quota is returned if needed
        })
    except Exception as e:
        return JsonResponse({'status': 'failure', 'message': str(e)})
