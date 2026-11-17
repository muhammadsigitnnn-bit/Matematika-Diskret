"""Relasi - Matematika Diskret (versi terminal, menu per halaman)
Jalankan: python relasi.py
"""
import re


# ---------- Parsing ----------
def parse_himpunan(teks):
    hasil = []
    for x in teks.replace("{", "").replace("}", "").split(","):
        x = x.strip()
        if x and x not in hasil:
            hasil.append(x)
    return hasil


def parse_relasi(teks):
    hasil = []
    for p in re.findall(r"\(\s*([^,()]+?)\s*,\s*([^,()]+?)\s*\)", teks):
        if p not in hasil:
            hasil.append(p)
    return hasil


# ---------- Perhitungan ----------
def sifat_relasi(himpunan, r):
    s = set(r)
    refleksif = all((a, a) in s for a in himpunan)
    irefleksif = all((a, a) not in s for a in himpunan)
    simetris = all((y, x) in s for x, y in s)
    antisimetris = all(not ((y, x) in s and x != y) for x, y in s)
    asimetris = all((y, x) not in s for x, y in s)
    transitif = all((x, w) in s for x, y in s for z, w in s if y == z)
    return {
        "Refleksif": refleksif,
        "Irefleksif": irefleksif,
        "Simetris": simetris,
        "Anti-simetris": antisimetris,
        "Asimetris": asimetris,
        "Transitif": transitif,
        "Relasi ekuivalen": refleksif and simetris and transitif,
        "Relasi urutan parsial": refleksif and antisimetris and transitif,
    }


def analisis(a, b, r):
    s = set(r)
    return {
        "domain": [x for x in a if any(p[0] == x for p in r)],
        "daerah_hasil": [y for y in b if any(p[1] == y for p in r)],
        "matriks": [[1 if (x, y) in s else 0 for y in b] for x in a],
        "invers": [(y, x) for x, y in r],
        "fungsi": all(sum(1 for p in r if p[0] == x) == 1 for x in a),
        "total": len(a) * len(b),
        "sifat": sifat_relasi(a, r) if set(a) == set(b) else None,
    }


def fmt_set(arr):
    return "{" + ", ".join(arr) + "}"


def fmt_pairs(arr):
    return "{" + ", ".join(f"({x}, {y})" for x, y in arr) + "}"


# ---------- Halaman ----------
def garis(judul):
    print("\n" + "=" * 56)
    print(judul.center(56))
    print("=" * 56)


def halaman_pengertian():
    garis("PENGERTIAN RELASI")
    print("""
1. APA ITU RELASI?
   Relasi berarti hubungan, misalnya siswa dengan mata pelajaran
   yang ia ambil. Dalam matematika diskret, hubungan itu ditulis
   sebagai kumpulan pasangan. Jika Ani mengambil Fisika, ditulis
   (Ani, Fisika). Mudahnya: relasi = daftar pasangan yang
   "berhubungan".

2. PASANGAN TERURUT DAN HASIL KALI KARTESIUS
   Pasangan terurut (a, b) memperhatikan urutan: (1, 2) beda
   dengan (2, 1).
   A x B = {(a, b) | a di A dan b di B}
   Contoh: A = {1, 2}, B = {x, y}
           A x B = {(1,x), (1,y), (2,x), (2,y)}, banyaknya 2 x 2 = 4.

3. DEFINISI RELASI
   Relasi dari A ke B adalah himpunan bagian dari A x B.
       R subset A x B     (a, b) di R  <=>  a R b
   - Relasi boleh kosong, dan boleh berisi seluruh A x B.
   - Relasi pada himpunan A berarti R subset A x A.
   - Jika |A| = m dan |B| = n, ada 2^(m*n) relasi yang mungkin,
     karena tiap pasangan bisa "dipakai" atau "tidak dipakai".

4. DOMAIN, KODOMAIN, DAERAH HASIL
   - Domain       : anggota A yang muncul sebagai elemen pertama.
   - Kodomain     : seluruh himpunan B.
   - Daerah hasil : anggota B yang muncul sebagai elemen kedua.
   Mudahnya: domain = siapa saja yang punya pasangan, daerah hasil
   = siapa saja yang dipilih sebagai pasangan.

5. CARA MENYAJIKAN RELASI
   - Himpunan pasangan : {(1,x), (2,y), (3,x), (3,y)}
   - Tabel             : dua kolom, elemen A dan pasangannya di B.
   - Diagram panah     : panah dari a ke b untuk tiap (a, b) di R.
   - Matriks relasi    : baris untuk A, kolom untuk B, isi 1 jika
                         (a, b) di R dan 0 jika tidak.
   - Graf berarah      : tiap anggota A jadi titik, tiap (a, b)
                         jadi panah. Pasangan (a, a) jadi loop.

6. INVERS RELASI
   R^-1 = {(b, a) | (a, b) di R}   (semua pasangan dibalik)
   Domain R^-1 = daerah hasil R, dan sebaliknya. Pada matriks,
   invers sama dengan transpos.

7. KOMPOSISI RELASI
   R dari A ke B, S dari B ke C.
   S o R = {(a, c) | ada b: (a, b) di R dan (b, c) di S}
   Mudahnya: komposisi itu "lewat perantara". R dikerjakan dulu,
   baru S.

8. OPERASI HIMPUNAN PADA RELASI
   Gabungan (R1 u R2), irisan (R1 n R2), selisih (R1 - R2), dan
   komplemen (A x B - R).

9. RELASI DAN FUNGSI
   Fungsi adalah relasi dengan syarat setiap anggota A punya
   TEPAT SATU pasangan di B. Semua fungsi adalah relasi, tetapi
   tidak semua relasi adalah fungsi.

10. CLOSURE (PENUTUP) RELASI
   Closure suatu sifat adalah relasi terkecil yang memuat R dan
   memiliki sifat itu.
   - Closure refleksif : tambahkan (a, a) untuk semua a di A.
   - Closure simetris  : tambahkan (b, a) untuk tiap (a, b) di R.
   - Closure transitif : tambahkan (a, c) setiap ada (a, b) dan
                         (b, c), ulangi sampai tidak ada yang kurang.

11. RELASI EKUIVALEN DAN URUTAN PARSIAL
   - Relasi ekuivalen: refleksif, simetris, transitif. Artinya
     "sama dalam suatu hal" dan membagi A menjadi kelas-kelas
     ekuivalen yang tidak tumpang tindih.
   - Urutan parsial: refleksif, anti-simetris, transitif. Tidak
     semua pasangan harus bisa dibandingkan.
""")


def halaman_contoh():
    garis("CONTOH RELASI")
    print("""
Contoh 1: hasil kali kartesius dan banyak relasi
  A = {a, b}, B = {1, 2, 3}
  A x B = {(a,1), (a,2), (a,3), (b,1), (b,2), (b,3)}
  |A x B| = 2 x 3 = 6, jadi banyak relasi = 2^6 = 64.
  Dua di antaranya: R = {} dan R = A x B.

Contoh 2: siswa dan mata pelajaran
  A = {Ani, Budi}, B = {Fisika, Kimia, Biologi}
  R = {(Ani, Fisika), (Ani, Kimia), (Budi, Biologi)}
  Domain       = {Ani, Budi}
  Daerah hasil = {Fisika, Kimia, Biologi}
  Invers = {(Fisika, Ani), (Kimia, Ani), (Biologi, Budi)}
  Bukan fungsi, karena Ani punya dua pasangan.

Contoh 3: matriks relasi
  A = {1, 2, 3}, B = {x, y}
  R = {(1,x), (2,y), (3,x), (3,y)}
        x  y
     1  1  0
     2  0  1
     3  1  1
  Jumlah angka 1 = |R| = 4.

Contoh 4: "habis membagi"
  A = {1, 2, 3, 4}
  R = {(1,1), (1,2), (1,3), (1,4), (2,2), (2,4), (3,3), (4,4)}
  Refleksif       : (1,1), (2,2), (3,3), (4,4) semuanya ada.
  Tidak simetris  : (1,2) ada, tetapi (2,1) tidak ada.
  Anti-simetris   : tidak ada dua bilangan berbeda saling membagi.
  Transitif       : (1,2) dan (2,4) ada, (1,4) juga ada.
  -> relasi urutan parsial (bukan urutan total, karena 2 dan 3
     tidak bisa dibandingkan).

Contoh 5: "lebih kecil dari"
  A = {1, 2, 3}, R = {(1,2), (1,3), (2,3)}
  Irefleksif, tidak simetris, asimetris, anti-simetris (hampa),
  dan transitif. Asimetris pasti irefleksif dan anti-simetris.

Contoh 6: relasi ekuivalen (kongruen modulo 3)
  A = {1, 2, 3, 4, 5, 6}, a R b jika sisa bagi 3 sama.
  R = {(1,1), (1,4), (4,1), (4,4), (2,2), (2,5), (5,2), (5,5),
       (3,3), (3,6), (6,3), (6,6)}
  Refleksif, simetris, transitif -> relasi ekuivalen.
  Kelas ekuivalen: {1, 4}, {2, 5}, {3, 6}.

Contoh 7: simetris tetapi tidak transitif
  A = {Ani, Budi, Cici}, relasi "berteman"
  R = {(Ani,Budi), (Budi,Ani), (Budi,Cici), (Cici,Budi)}
  Simetris dan irefleksif. Tidak transitif: (Ani,Budi) dan
  (Budi,Cici) ada, tetapi (Ani,Cici) tidak ada.

Contoh 8: memeriksa sifat lewat matriks
  A = {1, 2, 3}, R = {(1,1), (2,2), (3,3), (1,2), (2,1)}
        1  2  3
     1  1  1  0
     2  1  1  0
     3  0  0  1
  Diagonal semua 1 -> refleksif. Matriks sama dengan transposnya
  -> simetris. Transitif juga terpenuhi.
  -> relasi ekuivalen dengan kelas {1, 2} dan {3}.

Contoh 9: invers relasi
  A = {1, 2, 3}, B = {a, b}, R = {(1,a), (2,b), (3,a)}
  R^-1 = {(a,1), (b,2), (a,3)}
  Domain dan daerah hasil tertukar.

Contoh 10: komposisi relasi
  A = {1, 2, 3}, B = {a, b}, C = {x, y}
  R = {(1,a), (2,b), (3,a)}
  S = {(a,x), (b,y), (b,x)}
  (1,a),(a,x) -> (1,x)
  (2,b),(b,y) -> (2,y)    (2,b),(b,x) -> (2,x)
  (3,a),(a,x) -> (3,x)
  S o R = {(1,x), (2,x), (2,y), (3,x)}

Contoh 11: operasi dan closure
  A = {1, 2}, R1 = {(1,1), (1,2), (2,2)}, R2 = {(1,2), (2,1)}
  R1 u R2 = {(1,1), (1,2), (2,1), (2,2)}
  R1 n R2 = {(1,2)}
  R1 - R2 = {(1,1), (2,2)}
  Komplemen R1 = {(2,1)}

  A = {1, 2, 3}, R = {(1,2), (2,3)}
  Closure refleksif : tambah (1,1), (2,2), (3,3)
  Closure simetris  : tambah (2,1), (3,2)
  Closure transitif : tambah (1,3) -> {(1,2), (2,3), (1,3)}

Contoh 12: fungsi dan bukan fungsi
  A = {1, 2, 3}, B = {a, b}
  R1 = {(1,a), (2,b), (3,b)}  -> fungsi (tiap anggota A punya
                                 tepat satu pasangan)
  R2 = {(1,a), (1,b), (2,a)}  -> bukan fungsi (1 punya dua
                                 pasangan, 3 tidak punya)
  Banyak fungsi A ke B = 2^3 = 8, banyak relasi = 2^6 = 64.
""")


def halaman_sifat():
    garis("SIFAT RELASI PADA SATU HIMPUNAN")
    print("""
- Refleksif         : (a, a) di R untuk setiap a di A.
- Irefleksif        : (a, a) tidak di R untuk setiap a di A.
- Simetris          : jika (a, b) di R maka (b, a) di R.
- Anti-simetris     : jika (a, b) dan (b, a) di R maka a = b.
- Asimetris         : jika (a, b) di R maka (b, a) tidak di R.
- Transitif         : jika (a, b) dan (b, c) di R maka (a, c) di R.
- Relasi ekuivalen  : refleksif, simetris, dan transitif.
- Urutan parsial    : refleksif, anti-simetris, dan transitif.
""")


def halaman_kalkulator():
    garis("KALKULATOR RELASI")
    print("Contoh: A = 1, 2, 3, 4   R = (1,1), (1,2), (2,2), (3,3), (4,4)")
    while True:
        a = parse_himpunan(input("\nHimpunan A: "))
        if not a:
            print("Himpunan A tidak boleh kosong.")
            continue
        b = parse_himpunan(input("Himpunan B (kosong = sama dengan A): ")) or a
        r = parse_relasi(input("Relasi R: "))

        luar = [p for p in r if p[0] not in a or p[1] not in b]
        if luar:
            print("Pasangan di luar A x B:", fmt_pairs(luar))
            continue

        h = analisis(a, b, r)
        print("\n--- Hasil ---")
        print("A            :", fmt_set(a))
        print("B            :", fmt_set(b))
        print("R            :", fmt_pairs(r))
        print(f"|R|          : {len(r)} dari {h['total']} pasangan di A x B")
        print("Domain       :", fmt_set(h["domain"]))
        print("Kodomain     :", fmt_set(b))
        print("Daerah hasil :", fmt_set(h["daerah_hasil"]))
        print("Invers R^-1  :", fmt_pairs(h["invers"]))
        print("Fungsi?      :", "Ya" if h["fungsi"] else "Tidak")
        print(f"Relasi yang mungkin: 2^{h['total']} = {2 ** h['total']}")

        print("\nMatriks relasi:")
        lebar = max(len(x) for x in a + b) + 2
        print(" " * lebar + "".join(y.ljust(lebar) for y in b))
        for x, baris in zip(a, h["matriks"]):
            print(x.ljust(lebar) + "".join(str(v).ljust(lebar) for v in baris))

        if h["sifat"]:
            print("\nSifat relasi:")
            for nama, nilai in h["sifat"].items():
                print(f"  {nama:<22}: {'Ya' if nilai else 'Tidak'}")
        else:
            print("\nSifat relasi hanya diperiksa jika A = B.")

        if input("\nHitung lagi? (y/n): ").strip().lower() != "y":
            break


# ---------- Menu utama ----------
MENU = {
    "1": ("Pengertian relasi", halaman_pengertian),
    "2": ("Contoh relasi", halaman_contoh),
    "3": ("Sifat relasi", halaman_sifat),
    "4": ("Kalkulator relasi", halaman_kalkulator),
}


def main():
    while True:
        garis("RELASI - MATEMATIKA DISKRET")
        for kode, (nama, _) in MENU.items():
            print(f"  [{kode}] {nama}")
        print("  [0] Keluar")
        pilih = input("\nPilih halaman: ").strip()
        if pilih == "0":
            print("Sampai jumpa!")
            break
        if pilih in MENU:
            MENU[pilih][1]()
            input("\nTekan Enter untuk kembali ke menu...")
        else:
            print("Pilihan tidak ada, coba lagi.")


if __name__ == "__main__":
    main()
