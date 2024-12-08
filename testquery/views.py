from django.shortcuts import render
from utils.query import query

# Create your views here.
def show_pengguna(request):
    #Buat query
    query_str = f"""
    select * from kategori_jasa
    where id_kategori_jasa = '49847c0d-0fa7-4012-9c7e-6840f5454c13'
    """
    
    #Masukkan string query
    hasil = query(query_str)
    print(hasil)
    context={
        'list_pengguna': hasil
    }
    print(context['list_pengguna'])
    return render(request, 'pengguna.html', context)
