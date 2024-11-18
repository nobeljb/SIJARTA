from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.http import Http404, HttpResponse
from django import forms

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

# View for Testimony Form
def testimoni_form(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")
        worker_name = "Worker Name"  # Replace with dynamic data if available

        # Add the new testimony to the list
        testimonies.append({
            "user_name": user_name,
            "date": datetime.today().strftime("%Y-%m-%d"),
            "testimony_text": comment,
            "worker_name": worker_name,
            "rating": rating
        })

        # Redirect to the testimony cards page
        return redirect("testimoni_cards")

    return render(request, "testimoni_form.html")

# View for Testimony Cards
def testimoni_cards(request):
    return render(request, "testimoni_cards.html", {"testimonies": testimonies})

# View for Discounts and Promotions
def diskon(request):
    # Sample voucher data
    vouchers = [
        {
            "code": "SAVE50",
            "discount": "50%",
            "min_transaction": "Rp 100000",
            "remaining_days": 5,
            "quota": 50,
            "price": 50000000
        },
        {
            "code": "DISCOUNT20",
            "discount": "20%",
            "min_transaction": "Rp 5000",
            "remaining_days": 10,
            "end_date": "28 November 2024",
            "quota": 30,
            "price": 50
        }
    ]

    # Sample promo data
    promos = [
        {"code": "FREESHIP", "end_date": "2024-12-31"},
        {"code": "NEWYEAR50", "end_date": "2025-01-01"}
    ]

    return render(request, 'diskon.html', {"vouchers": vouchers, "promos": promos})

# View for Voucher Purchase Confirmation
def pembelian_voucher(request):
    if request.method == "POST":
        voucher_code = request.POST.get("voucher_code")
        balance = float(request.POST.get("balance", 0))
        price = float(request.POST.get("price", 0))
        end_date = request.POST.get("end_date")
        quota = int(request.POST.get("quota", 0))

        if balance >= price:
            message = f"""
                Selamat! Anda berhasil membeli voucher dengan kode {voucher_code}.
                Voucher ini akan berlaku hingga tanggal {end_date} dengan kuota penggunaan sebanyak {quota} kali.
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
