from django.shortcuts import render, redirect
from django.contrib import messages


#Dummy Pengguna
pengguna = [
    {
        'role': 'pengguna',
        'nama': 'Kaela Kovalskia',
        'password': 'kaela123',
        'level': '69',
        'jenis_kelamin': 'Perempuan',
        'nohp': '123456789',
        'tanggal_lahir': '30-08-2004',
        'alamat': 'Jalan Kita Masih Panjang',
        'saldo': '11111'
    },
    {   
        'role': 'pekerja',
        'nama': 'Vestia Zeta',
        'password': 'zeta123',
        'Level': '77',
        'jenis_kelamin': 'perempuan',
        'nohp': '1122334455',
        'tanggal_lahir': '11-7-2001',
        'nama_bank': 'OVO',
        'rekening': '123456',
        'npwp': '345567',
        'foto': 'ini foto',
        'alamat': 'Jalan in aja dulu',
        'saldo': '22222',
        'rating': '5',
        'jumlah_pesanan': '1',
        'kategori_pekerjaan': 'Kategori Jasa 1'
    }
]

penggunalogin = {}

def show_profile(request):
    global penggunalogin
    if(penggunalogin['role'] == 'pengguna'):
        return render(request, "profile_pengguna.html", penggunalogin)
    return render(request, "profile_pekerja.html", penggunalogin)

def choose_role(request):
    return render(request, "choose_role.html")

def register_pekerja(request):
    if request.method == 'POST':
        nohp = request.POST.get('nohp')
        nama_bank = request.POST.get('nama_bank')
        rekening = request.POST.get('rekening')
        npwp = request.POST.get('npwp')

        # Validasi No HP harus unik
        for user in pengguna:
            if user['nohp'] == nohp:
                return render(request, 'register_pekerja.html', {
                    'error_message': 'Nomor HP sudah terdaftar. Silakan login.'
                })

            # Validasi kombinasi nama bank dan rekening harus unik
            if user.get('nama_bank') == nama_bank and user.get('rekening') == rekening:
                return render(request, 'register_pekerja.html', {
                    'error_message': 'Kombinasi Nama Bank dan No Rekening sudah terdaftar.'
                })

            # Validasi NPWP harus unik
            if user.get('npwp') == npwp:
                return render(request, 'register_pekerja.html', {
                    'error_message': 'NPWP sudah terdaftar.'
                })

        # Jika semua validasi lolos, tambahkan data ke pengguna
        data = {
            'role': 'pekerja',
            'nama': request.POST.get('nama'),
            'password': request.POST.get('password'),
            'jenis_kelamin': request.POST.get('jenis_kelamin'),
            'nohp': nohp,
            'tanggal_lahir': request.POST.get('tanggal_lahir'),
            'alamat': request.POST.get('alamat'),
            'nama_bank': nama_bank,
            'rekening': rekening,
            'npwp': npwp,
            'foto': request.POST.get('foto'),
        }
        pengguna.append(data)

        return render(request, 'success.html', {'message': 'Pendaftaran berhasil.'})

    # Dropdown Nama Bank
    bank_list = ['GoPay', 'OVO', 'Virtual Account BCA', 'Virtual Account BNI', 'Virtual Account Mandiri']
    return render(request, 'register_pekerja.html', {'bank_list': bank_list})

def register_pengguna(request):
    if request.method == 'POST':
        nohp = request.POST.get('nohp')

        # Validasi No HP harus unik
        for user in pengguna:
            if user['nohp'] == nohp:
                return render(request, 'register_pengguna.html', {
                    'error_message': 'Nomor HP sudah terdaftar. Silakan login.'
                })

        # Jika validasi lolos, tambahkan data ke pengguna
        data = {
            'role': 'pengguna',
            'nama': request.POST.get('nama'),
            'password': request.POST.get('password'),
            'jenis_kelamin': request.POST.get('role'),  # sesuai dengan name di radio button
            'nohp': nohp,
            'tanggal_lahir': request.POST.get('tanggal_lahir'),
            'alamat': request.POST.get('alamat'),
            'saldo': '0'  # Saldo awal
        }
        pengguna.append(data)

        return render(request, 'success.html', {'message': 'Pendaftaran berhasil.'})

    return render(request, 'register_pengguna.html')

def login(request):
    if request.method == 'POST':
        nohp = request.POST.get('nohp')
        password = request.POST.get('password')

        global penggunalogin
        penggunalogin = {}
        
        # Cek kredensial
        for user in pengguna:
            if user['nohp'] == nohp and user['password'] == password:
                # Simpan data pengguna yang login ke penggunalogin
                
                penggunalogin = user
                print(penggunalogin)
                
                messages.success(request, f"Selamat datang, {user['nama']}!")
                return redirect('kuning:show_profile')  # Redirect ke halaman profile
        
        # Jika kredensial tidak cocok
        messages.error(request, 'Nomor HP atau Password salah!')
        return render(request, 'login.html')
    
    return render(request, 'login.html')

def logout(request):
    global penggunalogin
    penggunalogin = {}
    messages.success(request, 'Berhasil logout!')
    return redirect('kuning:login')