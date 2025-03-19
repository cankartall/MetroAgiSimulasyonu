from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        # İstasyon bilgilerini tutan sınıf
        self.idx = idx  # İstasyon kimliği
        self.ad = ad  # İstasyon adı
        self.hat = hat  # İstasyonun bağlı olduğu hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # Komşu istasyonlar ve süre bilgisi

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        # İstasyona bir komşu ekleyen fonksiyon
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        # Metro ağını temsil eden sınıf
        self.istasyonlar: Dict[str, Istasyon] = {}  # Tüm istasyonları kimlikleri ile saklayan sözlük
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)  # Hatlara göre istasyonları saklayan sözlük

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        # Yeni bir istasyon ekleyen fonksiyon
        if idx not in self.istasyonlar: #istasyon yoksa
            istasyon = Istasyon(idx, ad, hat)  # Yeni istasyon nesnesi oluşturuluyor
            self.istasyonlar[idx] = istasyon  # İstasyon sözlüğüne ekleniyor
            self.hatlar[hat].append(istasyon)  # Hat bazlı istasyon listesine ekleniyor

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        # İki istasyon arasında bağlantı ekleyen fonksiyon
        istasyon1 = self.istasyonlar[istasyon1_id]  # İlk istasyon nesnesi alınıyor
        istasyon2 = self.istasyonlar[istasyon2_id]  # İkinci istasyon nesnesi alınıyor
        istasyon1.komsu_ekle(istasyon2, sure)  # İki yönlü bağlantı ekleniyor
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        # En az aktarma ile iki istasyon arasındaki yolu bulan fonksiyon (BFS algoritması kullanıyor)
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        kuyruk = deque([(baslangic, [baslangic])])  # BFS için kuyruk kullanılıyor
        ziyaret_edildi = set()

        while kuyruk:
            mevcut, yol = kuyruk.popleft()  # Kuyruğun başındaki eleman çekiliyor
            if mevcut == hedef:
                return yol  # Hedefe ulaşıldığında yolu döndür
            
            for komsu, _ in mevcut.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)  # Ziyaret edilenler listesine ekleniyor
                    kuyruk.append((komsu, yol + [komsu]))  # Yeni yol kuyruğa ekleniyor
        
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        # En kısa sürede ulaşılacak rotayı bulan fonksiyon (A* algoritması)
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        pq = [(0, id(baslangic), baslangic, [baslangic])]  # Öncelik kuyruğu (süre bazlı sıralama)
        ziyaret_edildi = {}

        while pq:
            toplam_sure, _, mevcut, yol = heapq.heappop(pq)  # En düşük süreli düğüm seçiliyor
            if mevcut == hedef:
                return yol, toplam_sure  # Hedefe ulaşıldığında yolu ve süreyi döndür
            
            if mevcut in ziyaret_edildi and ziyaret_edildi[mevcut] <= toplam_sure:
                continue
            ziyaret_edildi[mevcut] = toplam_sure
            
            for komsu, sure in mevcut.komsular:
                heapq.heappush(pq, (toplam_sure + sure, id(komsu), komsu, yol + [komsu]))
        
        return None


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    print("\n=== Test Senaryoları ===")
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4") #İstasyonları en az aktarmalı fonksiyonuna gönderdik
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    print("\n4. Sıhhiye'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M3", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("M3", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    print("\n5. Gar'dan Ulus'a:")
    rota = metro.en_az_aktarma_bul("M4", "K2")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("M4", "K2")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

        print("\n6. Keçiören'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("T4", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("T4", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

        