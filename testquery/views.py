from django.shortcuts import render
from utils.query import query

# Create your views here.
def show_pengguna(request):
    #Buat query
    query_str = f"""
    insert into pengguna values(
    '8648d4f5-133d-4e74-a56d-85ec6dc93c3e', 'Test Trigger', 'P', '6238370331927445', 'test', '2004-09-02', 'Jalan', 2000.00)
    """
    
    #Masukkan string query
    hasil = query(query_str)
    print(hasil)
    context={
        'list_pengguna': hasil
    }
    print(context['list_pengguna'])
    return render(request, 'pengguna.html', context)
