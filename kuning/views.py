from django.shortcuts import render, redirect
from django.contrib import messages
from utils.query import query
import uuid
from datetime import datetime


def show_profile(request):
    penggunalogin = request.session.get('penggunalogin')
    context = {
        'penggunalogin': penggunalogin
    }
    if(penggunalogin['role'] == 'pengguna'):
        return render(request, "profile_pengguna.html", context)
    return render(request, "profile_pekerja.html", context)

def choose_role(request):
    return render(request, "choose_role.html")

def register_pekerja(request):
    if request.method == 'POST':
        id = uuid.uuid4()
        nama = request.POST.get('nama')
        pwd = request.POST.get('password')
        jeniskelamin = request.POST.get('jenis_kelamin')
        tgllahir = request.POST.get('tanggal_lahir')
        alamat = request.POST.get('alamat')
        foto = request.POST.get('foto')
        nohp = request.POST.get('nohp')
        nama_bank = request.POST.get('nama_bank')
        rekening = request.POST.get('rekening')
        npwp = request.POST.get('npwp')

        # Validasi No HP harus unik
        query_str = f"""
        select * from pengguna
        where nohp = '{nohp}'
        """
        hasil = query(query_str)
        if len(hasil) != 0:
            return render(request, 'login.html', {'message': 'Pengguna Sudah Terdaftar'})
        
        # Validasi kombinasi Nama Bank dan Nomor Rekening harus unik
        query_str =f"""
        select *
        from pekerja
        where namabank = '{nama_bank}'
        and nomorrekening = '{rekening}'
        """
        hasil = query(query_str)
        if len(hasil) != 0:
            return render(request, 'register_pekerja.html', {'message': 'Pengguna Sudah Terdaftar'})
        
        # Validasi NPWP harus unik
        query_str = f"""
        select * from pekerja
        where npwp = '{npwp}'
        """
        hasil = query(query_str)
        if len(hasil) != 0:
            return render(request, 'register_pekerja.html', {'message': 'Pengguna Sudah Terdaftar'})

        # Jika semua validasi lolos, tambahkan data ke tabel pengguna
        query_str = f"""
        insert into pengguna values(
        '{id}', '{nama}', '{jeniskelamin}', '{nohp}', '{pwd}', '{tgllahir}', '{alamat}')
        """
        hasil = query(query_str)

        # Insert ke tabel pekerja
        query_str = f"""
        insert into pekerja values(
        '{id}', '{nama_bank}', '{rekening}', '{npwp}', '{foto}')
        """
        hasil = query(query_str)

        return render(request, 'login.html', {'message': 'Pendaftaran berhasil.'})

    # Dropdown Nama Bank
    bank_list = ['GoPay', 'OVO', 'Virtual Account BCA', 'Virtual Account BNI', 'Virtual Account Mandiri']
    return render(request, 'register_pekerja.html', {'bank_list': bank_list})

def register_pengguna(request):
    if request.method == 'POST':
        id = uuid.uuid4()
        nama = request.POST.get('nama')
        pwd = request.POST.get('password')
        jeniskelamin = request.POST.get('jenis_kelamin')
        tgllahir = request.POST.get('tanggal_lahir')
        alamat = request.POST.get('alamat')
        nohp = request.POST.get('nohp')

        # Validasi No HP harus unik
        query_str = f"""
        select * from pengguna
        where nohp = '{nohp}'
        """
        hasil = query(query_str)
        if len(hasil) != 0:
            return render(request, 'login.html', {'message': 'Pengguna Sudah Terdaftar'})

        # Jika validasi lolos, tambahkan data ke pengguna
        query_str = f"""
        insert into pengguna values(
        '{id}', '{nama}', '{jeniskelamin}', '{nohp}', '{pwd}', '{tgllahir}', '{alamat}')
        """
        hasil = query(query_str)
        query_str = f"""
        insert into pelanggan values(
        '{id}')
        """
        hasil = query(query_str)

        return render(request, 'login.html', {'message': 'Pendaftaran berhasil.'})

    return render(request, 'register_pengguna.html')

def login(request):
    context = {
        'message': ''
    }
    if request.method == 'POST':
        nohp = request.POST.get('nohp')
        password = request.POST.get('password')

        query_str = f"""
        SELECT * FROM pengguna
        where nohp = '{nohp}'
        and pwd = '{password}'
        """
        hasil = query(query_str)
        if len(hasil) == 1:
            penggunalogin = {
                'id_user': str(hasil[0]['id_user']),  # Convert UUID to string
                'nama': hasil[0]['nama'],
                'jeniskelamin': hasil[0]['jeniskelamin'],
                'nohp': hasil[0]['nohp'],
                'pwd': hasil[0]['pwd'],
                'tgllahir': hasil[0]['tgllahir'].isoformat(),  # Convert date to string (ISO format)
                'alamat': hasil[0]['alamat'],
                'saldomypay': str(hasil[0]['saldomypay'])  # Convert Decimal to string
            }

            query_str=f"""
            select * from pekerja
            where id_pekerja = '{penggunalogin['id_user']}'
            """
            pekerja = query(query_str)

            # Validasi role
            if len(pekerja) == 1:
                penggunalogin['role'] = 'pekerja'
                penggunalogin['namabank'] = pekerja[0]['namabank']
                penggunalogin['nomorrekening'] = pekerja[0]['nomorrekening']
                penggunalogin['npwp'] = pekerja[0]['npwp']
                penggunalogin['foto'] = pekerja[0]['linkfoto']
                penggunalogin['rating'] = str(pekerja[0]['rating'])
                penggunalogin['jmlpesananselesai'] = str(pekerja[0]['jmlpesananselesai'])

                query_str = f"""
                select * from kategori_jasa kj, pekerja_kategori_jasa pkj
                where pkj.pekerjaid = '{penggunalogin['id_user']}'
                and pkj.kategorijasaid = kj.id_kategori_jasa
                """
                kategori = query(query_str)
                penggunalogin['kategori']=[]
                for row in kategori:
                    penggunalogin['kategori'].append(row['namakategori'])
            else:
                query_str = f"""
                select * from pelanggan
                where id_pelanggan = '{penggunalogin['id_user']}'
                """
                pekerja = query(query_str)
                penggunalogin['role'] = 'pengguna'
                penggunalogin['level'] = pekerja[0]['level']
            
            print(penggunalogin)

            request.session['penggunalogin'] = penggunalogin
            context['penggunalogin'] = penggunalogin

            if penggunalogin['role'] == 'pekerja':
                return render(request, 'profile_pekerja.html', context)
            
            return render(request, 'profile_pengguna.html', context)
        context['message'] = 'Pengguna belum terdaftar'
    return render(request, 'login.html', context)

def logout(request):
    request.session.flush()
    messages.success(request, 'Berhasil logout!')
    return redirect('kuning:login')

def update_pekerja(request):
    penggunalogin = request.session.get('penggunalogin')
    if request.method == 'POST':
        id = penggunalogin['id_user']
        nama = request.POST.get('nama')
        jeniskelamin = request.POST.get('jenis_kelamin')
        nohp = request.POST.get('nohp')
        tgllahir = request.POST.get('tanggal_lahir')
        alamat = request.POST.get('alamat')
        namabank = request.POST.get('nama_bank')
        nomorrekening = request.POST.get('rekening')
        npwp = request.POST.get('npwp')
        foto = request.POST.get('foto')

        # Update data pada database
        query_str = f"""
        update pengguna
        set nama = '{nama}', jeniskelamin = '{jeniskelamin}', nohp = '{nohp}', tgllahir = '{tgllahir}', alamat = '{alamat}'
        where id_user = '{id}'
        """
        hasil = query(query_str)
        query_str = f"""
        update pekerja
        set namabank = '{namabank}', nomorrekening = '{nomorrekening}', npwp = '{npwp}', linkfoto = '{foto}'
        where id_pekerja = '{id}'
        """
        hasil = query(query_str)

        # Perbarui data pada session
        query_str = f"""
        SELECT * FROM pengguna
        where id_user = '{id}'
        """
        hasil = query(query_str)
        penggunaUpdate = {
            'id_user': str(hasil[0]['id_user']),  # Convert UUID to string
            'nama': hasil[0]['nama'],
            'jeniskelamin': hasil[0]['jeniskelamin'],
            'nohp': hasil[0]['nohp'],
            'pwd': hasil[0]['pwd'],
            'tgllahir': hasil[0]['tgllahir'].isoformat(),  # Convert date to string (ISO format)
            'alamat': hasil[0]['alamat'],
            'saldomypay': str(hasil[0]['saldomypay'])  # Convert Decimal to string
        }

        query_str=f"""
        select * from pekerja
        where id_pekerja = '{id}'
        """
        pekerja = query(query_str)
        penggunaUpdate['role'] = 'pekerja'
        penggunaUpdate['namabank'] = pekerja[0]['namabank']
        penggunaUpdate['nomorrekening'] = pekerja[0]['nomorrekening']
        penggunaUpdate['npwp'] = pekerja[0]['npwp']
        penggunaUpdate['foto'] = pekerja[0]['linkfoto']
        penggunaUpdate['rating'] = str(pekerja[0]['rating'])
        penggunaUpdate['jmlpesananselesai'] = str(pekerja[0]['jmlpesananselesai'])

        query_str = f"""
        select * from kategori_jasa kj, pekerja_kategori_jasa pkj
        where pkj.pekerjaid = '{penggunaUpdate['id_user']}'
        and pkj.kategorijasaid = kj.id_kategori_jasa
        """
        kategori = query(query_str)
        penggunaUpdate['kategori']=[]
        for row in kategori:
            penggunaUpdate['kategori'].append(row['namakategori'])
        
        request.session['penggunalogin'] = penggunaUpdate

        return redirect('kuning:show_profile')
    
    # Jika GET request, tampilkan form dengan data current user
    bank_list = ['GoPay', 'OVO', 'Virtual Account BCA', 'Virtual Account BNI', 'Virtual Account Mandiri']
    context = {
        'penggunalogin': penggunalogin,
        'bank_list': bank_list
    }
    
    return render(request, 'update_pekerja.html', context)

def update_pengguna(request):
    penggunalogin = request.session.get('penggunalogin')

    if request.method == 'POST':
        id = penggunalogin['id_user']
        nama = request.POST.get('nama') 
        jeniskelamin = request.POST.get('jenis_kelamin')
        nohp = request.POST.get('nohp')
        tgllahir = request.POST.get('tanggal_lahir')
        alamat = request.POST.get('alamat')

        # Update data pada database
        query_str = f"""
        update pengguna
        set nama = '{nama}', jeniskelamin = '{jeniskelamin}', nohp = '{nohp}', tgllahir = '{tgllahir}', alamat = '{alamat}'
        where id_user = '{id}'
        """
        hasil = query(query_str)
        print(hasil)

        # Update data pada session
        query_str = f"""
        SELECT * FROM pengguna
        where id_user = '{id}'
        """
        hasil = query(query_str)
        penggunaUpdate = {
            'id_user': str(hasil[0]['id_user']),  # Convert UUID to string
            'nama': hasil[0]['nama'],
            'jeniskelamin': hasil[0]['jeniskelamin'],
            'nohp': hasil[0]['nohp'],
            'pwd': hasil[0]['pwd'],
            'tgllahir': hasil[0]['tgllahir'].isoformat(),  # Convert date to string (ISO format)
            'alamat': hasil[0]['alamat'],
            'saldomypay': str(hasil[0]['saldomypay'])  # Convert Decimal to string
        }

        query_str = f"""
        select * from pelanggan
        where id_pelanggan = '{id}'
        """
        pekerja = query(query_str)
        penggunaUpdate['role'] = 'pengguna'
        penggunaUpdate['level'] = pekerja[0]['level']

        request.session['penggunalogin'] = penggunaUpdate

        return redirect('kuning:show_profile')
    
    # Jika GET request, tampilkan form dengan data current user
    context = {
        'penggunalogin': penggunalogin
    }
    
    return render(request, 'update_pengguna.html', context)