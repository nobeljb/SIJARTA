from django.shortcuts import render
from utils.query import query

# Create your views here.
def show_pengguna(request):
    #Buat query
    query_str = f"""
    select * from kategori_jasa
    """
    
    #Masukkan string query
    hasil = query(query_str)
    print(hasil)
    context={
        'list_pengguna': hasil
    }
    print(context['list_pengguna'])
    return render(request, 'pengguna.html', context)
