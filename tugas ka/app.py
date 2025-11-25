from flask import Flask, render_template, request

# Inisialisasi aplikasi Flask. Objek 'app' ini yang akan dicari oleh Vercel.
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

RULES_LIST = [
    # Rules dengan 2 premis (lebih spesifik)
    (['P_system', 'P_performa'], 'C_cpp'),
    (['P_game', 'P_mahir'], 'C_csharp'),
    (['P_game', 'P_pemula'], 'C_pygame'),
    (['P_mobile', 'P_pemula'], 'C_flutter'),
    (['P_web', 'P_easy'], 'C_php'),
    
    # Rules dengan 1 premis (kurang spesifik/umum)
    (['P_mobile', 'P_cross'], 'C_flutter'),
    (['P_web'], 'C_js'),
    (['P_mobile'], 'C_kotlin'),
    (['P_AI'], 'C_python'),
    (['P_game'], 'C_csharp'),
    (['P_system'], 'C_cpp'),
    (['P_ds'], 'C_ds'),
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
        
        for rule in rules_to_check[:]:
            premis, hasil = rule
            
            if set(premis).issubset(facts):
                
                if hasil.startswith('C_') and hasil in proven:
                    rules_to_check.remove(rule)
                    continue

                if hasil.startswith('C_'):
                    proven.add(hasil)
                
                facts.add(hasil)
                
                rules_to_check.remove(rule)
                fired = True
        
        if not fired:
            break
            
    if proven:
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
        selected_codes = request.form.getlist('kriteria')
        
        if selected_codes:
            recommendations = forward_chaining(selected_codes)

    return render_template('index.html',
                           kriteria=KRITERIA,
                           recommendations=recommendations,
                           selected_codes=selected_codes)

# ===============================================
# CATATAN PENTING UNTUK DEPLOYMENT VERCEL
# ===============================================

# Baris di bawah ini WAJIB DIHAPUS/DIKOMENTARI saat deploy ke Vercel
# Karena Vercel menggunakan gunicorn/serverless runtime untuk menjalankan aplikasi.
# Jika Anda ingin menguji secara lokal:
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)