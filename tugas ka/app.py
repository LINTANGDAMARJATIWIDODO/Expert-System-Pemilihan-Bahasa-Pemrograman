from flask import Flask, render_template, request

app = Flask(__name__)

# ===============================================
# KRITERIA (PREMIS)
# ===============================================

KRITERIA = {
    'P_web': "Proyek Web",
    'P_mobile': "Proyek Mobile",
    'P_AI': "Proyek Artificial Intelligence",
    'P_game': "Proyek Game",
    'P_system': "Proyek Sistem",
    'P_cross': "Mobile Cross Platform",
    'P_performa': "Butuh Performa Tinggi",
    'P_pemula': "Pengalaman Pemula",
    'P_mahir': "Pengalaman Mahir",
    'P_ds': "Data Science",
    'P_easy': "Web yang Mudah Dipelajari"
}

# ===============================================
# KESIMPULAN (BAHASA PEMROGRAMAN)
# ===============================================

REKOMENDASI = {
    'C_js': "JavaScript (Frontend/Backend)",
    'C_kotlin': "Kotlin (Native Android/JVM)",
    'C_python': "Python (AI/Web Backend)",
    'C_cpp': "C++ (System/Game Engine)",
    'C_csharp': "C# (Unity)",
    'C_pygame': "Python (Pygame)",
    'C_flutter': "Flutter (Dart)",
    'C_php': "PHP (Web Backend)",
    'C_ds': "Python (Pandas, TensorFlow)"
}

# ===============================================
# ATURAN (RULE BASE) - DIURUTKAN UNTUK PRIORITAS SPESIFIK
# ===============================================

# List aturan dalam format: (premis, hasil).
# Diurutkan agar aturan dengan premis lebih banyak (lebih spesifik) dievaluasi duluan.
RULES_LIST = [
    # Rules dengan 2 premis (lebih spesifik)
    (['P_system', 'P_performa'], 'C_cpp'),    # R7
    (['P_game', 'P_mahir'], 'C_csharp'),      # R9
    (['P_game', 'P_pemula'], 'C_pygame'),     # R8
    (['P_mobile', 'P_pemula'], 'C_flutter'),  # R12
    (['P_web', 'P_easy'], 'C_php'),           # R11
    
    # Rules dengan 1 premis (kurang spesifik/umum)
    (['P_mobile', 'P_cross'], 'C_flutter'),   # R6 (Diubah ke Flutter agar konsisten dengan R12/Cross Platform)
    (['P_web'], 'C_js'),                      # R1
    (['P_mobile'], 'C_kotlin'),               # R2
    (['P_AI'], 'C_python'),                   # R3
    (['P_game'], 'C_csharp'),                 # R4
    (['P_system'], 'C_cpp'),                  # R5
    (['P_ds'], 'C_ds'),                       # R10
]

# Urutkan secara Descending berdasarkan jumlah premis
RULES_LIST.sort(key=lambda x: len(x[0]), reverse=True)


# ===============================================
# FORWARD CHAINING
# ===============================================

def forward_chaining(selected_criteria_codes):
    """Mengeksekusi penalaran Forward Chaining dengan prioritas spesifisitas."""
    facts = set(selected_criteria_codes)
    proven = set()
    rules_to_check = RULES_LIST[:] 
    
    while rules_to_check:
        fired = False
        
        # Iterasi pada salinan list untuk menghindari error modifikasi
        for rule in rules_to_check[:]:
            premis, hasil = rule
            
            # Cek apakah semua premis terpenuhi
            if set(premis).issubset(facts):
                
                # Jika hasil adalah kesimpulan dan sudah ada, abaikan
                if hasil.startswith('C_') and hasil in proven:
                    rules_to_check.remove(rule)
                    continue

                # Tambahkan hasil ke proven jika itu adalah kesimpulan (C_)
                if hasil.startswith('C_'):
                    proven.add(hasil)
                
                # Tambahkan hasil ke fakta (untuk aturan berantai)
                facts.add(hasil)
                
                # Hapus aturan yang sudah dieksekusi
                rules_to_check.remove(rule)
                fired = True
        
        # Hentikan jika tidak ada aturan yang dieksekusi dalam satu iterasi
        if not fired:
            break
            
    if proven:
        # Kembalikan nama bahasa pemrograman yang terbukti
        return [REKOMENDASI[c] for c in proven]

    return ["Tidak ditemukan bahasa pemrograman yang cocok. Pilih kriteria lain."]

# ===============================================
# ROUTING
# ===============================================

@app.route('/', methods=['GET', 'POST'])
def diagnose():
    """Menangani tampilan utama dan hasil diagnosis."""
    recommendations = None
    selected_codes = []

    if request.method == 'POST':
        # Ambil semua kode kriteria yang dipilih dari formulir
        selected_codes = request.form.getlist('kriteria')
        
        # Jika ada kriteria yang dipilih, jalankan forward chaining
        if selected_codes:
            recommendations = forward_chaining(selected_codes)

    return render_template('index.html',
                           kriteria=KRITERIA,
                           recommendations=recommendations,
                           selected_codes=selected_codes)

if __name__ == '__main__':
    # Pastikan Anda sudah membuat folder 'templates' berisi 'index.html' 
    # dan folder 'static' berisi 'style.css'
    print("Aplikasi berjalan di http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)