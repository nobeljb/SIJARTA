from django.shortcuts import render, redirect
from django.http import Http404
from utils.query import query
from datetime import datetime, timedelta
import uuid

# View for Testimony Form
def testimoni_form(request):
    if request.method == "POST":
        idtrpemesanan = request.POST.get("idtrpemesanan")  # ID of the related order
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        # Insert the new testimony into the database
        query_str = f"""
        INSERT INTO testimoni (idtrpemesanan, tgl, teks, rating)
        VALUES ('{idtrpemesanan}', '{datetime.today().strftime('%Y-%m-%d')}', '{comment}', {rating});
        """
        query(query_str)

        return redirect("testimoni_cards")

    return render(request, "testimoni_form.html")


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
    if request.method == "POST":
        voucher_code = request.POST.get("voucher_code")
        idpelanggan = request.POST.get("idpelanggan")  # UUID of the customer
        idmetodebayar = request.POST.get("idmetodebayar")  # UUID of the payment method
        
        # Fetch voucher details
        query_voucher = f"""
        SELECT harga AS price, jmlhariberlaku AS duration 
        FROM voucher 
        WHERE kode_voucher = '{voucher_code}';
        """
        voucher_data = query(query_voucher)
        if not voucher_data:
            return render(request, "pembelian_voucher.html", {
                "message": "Voucher tidak ditemukan.",
                "status": "failure"
            })
        
        price = float(voucher_data[0]["price"])
        duration = int(voucher_data[0]["duration"])
        
        # Fetch user balance
        query_user = f"""
        SELECT saldomypay 
        FROM pengguna 
        WHERE id_user = '{idpelanggan}';
        """
        user_data = query(query_user)
        if not user_data:
            return render(request, "pembelian_voucher.html", {
                "message": "Pengguna tidak ditemukan.",
                "status": "failure"
            })

        balance = float(user_data[0].get("saldomypay"))

        # Check if balance is sufficient
        if balance >= price:
            # Deduct balance and update user's saldomypay
            new_balance = balance - price
            update_balance_query = f"""
            UPDATE pengguna 
            SET saldomypay = {new_balance}
            WHERE id_user = '{idpelanggan}';
            """
            query(update_balance_query)

            # Calculate voucher validity dates
            today = datetime.today().date()
            end_date = today + timedelta(days=duration)

            # Insert purchase record into tr_pembelian_voucher
            id_tr_pembelian_voucher = str(uuid.uuid4())
            insert_purchase_query = f"""
            INSERT INTO tr_pembelian_voucher (
                id_tr_pembelian_voucher, tglawal, tglakhir, telahdigunakan, 
                idpelanggan, idvoucher, idmetodebayar
            ) VALUES (
                '{id_tr_pembelian_voucher}', '{today}', '{end_date}', 0, 
                '{idpelanggan}', '{voucher_code}', '{idmetodebayar}'
            );
            """
            query(insert_purchase_query)

            message = f"""
                Selamat! Anda berhasil membeli voucher dengan kode {voucher_code}.
                Voucher ini berlaku hingga tanggal {end_date}.
            """
            status = "success"
        else:
            message = "Maaf, saldo Anda tidak cukup untuk membeli voucher ini."
            status = "failure"

        return render(request, "pembelian_voucher.html", {
            "message": message,
            "status": status
        })

    raise Http404("Invalid request method")
