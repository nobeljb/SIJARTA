from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from decimal import Decimal

# Dummy data - in real implementation, this would come from SQL server
DUMMY_USER = {
    'phone_number': '081234567890',
    'balance': Decimal('1500000.00')
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

def show_mypay(request):
    """
    View for MyPay dashboard displaying user balance and transaction history
    Currently using dummy data, will be replaced with SQL server data later
    """
    paginator = Paginator(DUMMY_TRANSACTIONS, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'phone_number': DUMMY_USER['phone_number'],
        'balance': DUMMY_USER['balance'],
        'transactions': page_obj,
    }
    return render(request, 'dashboard.html', context)