"""
TÜRK Programlama Dili - Yorumlayıcı (Interpreter)
AST düğümlerini çalıştırır
"""

from typing import Dict, List, Any, Optional, Callable
from turk.ast import *


class YorumlayiciHata(Exception):
    def __init__(self, mesaj: str):
        self.mesaj = mesaj
        super().__init__(mesaj)


class KontrolAkisi(Exception):
    """Döngü kontrol akışı için özel durumlar"""
    pass


class DurHatasi(KontrolAkisi):
    pass


class DevamHatasi(KontrolAkisi):
    pass


class DonHatasi(KontrolAkisi):
    def __init__(self, deger: Any = None):
        self.deger = deger


class Kapsam:
    """Değişken kapsamı yönetimi"""
    def __init__(self, ust: Optional['Kapsam'] = None):
        self.ust = ust
        self.degiskenler: Dict[str, Any] = {}
        self.tipler: Dict[str, str] = {}

    def atama_yap(self, ad: str, deger: Any, tip: str = None):
        # Mevcut kapsamda veya üst kapsamlarda varsa güncelle
        if ad in self.degiskenler:
            self.degiskenler[ad] = deger
            if tip:
                self.tipler[ad] = tip
        elif self.ust:
            self.ust.atama_yap(ad, deger, tip)
        else:
            # Yoksa mevcut kapsama ekle
            self.degiskenler[ad] = deger
            if tip:
                self.tipler[ad] = tip

    def deger_oku(self, ad: str) -> Any:
        if ad in self.degiskenler:
            return self.degiskenler[ad]
        if self.ust:
            return self.ust.deger_oku(ad)
        raise YorumlayiciHata(f"Tanımlanmamış değişken: '{ad}'")

    def tip_oku(self, ad: str) -> Optional[str]:
        if ad in self.tipler:
            return self.tipler[ad]
        if self.ust:
            return self.ust.tip_oku(ad)
        return None

    def var_mi(self, ad: str) -> bool:
        if ad in self.degiskenler:
            return True
        if self.ust:
            return self.ust.var_mi(ad)
        return False


class YerlesikFonksiyon:
    """Yerleşik fonksiyon tanımı"""
    def __init__(self, ad: str, fonk: Callable, param_sayisi: int = -1):
        self.ad = ad
        self.fonk = fonk
        self.param_sayisi = param_sayisi


class Yorumlayici:
    def __init__(self):
        self.kuresel_kapsam = Kapsam()
        self.fonksiyonlar: Dict[str, Any] = {}
        self.cikti: List[str] = []
        self.girdi_kaynagi: Optional[List[str]] = None
        self.girdi_pozisyon = 0
        self._yerlesik_fonksiyonlar()

    def _yerlesik_fonksiyonlar(self):
        """Yerleşik fonksiyonları kaydet"""
        self.fonksiyonlar["yazdir"] = YerlesikFonksiyon("yazdir", self._fn_yazdir, 1)
        self.fonksiyonlar["oku"] = YerlesikFonksiyon("oku", self._fn_oku, 0)
        self.fonksiyonlar["uzunluk"] = YerlesikFonksiyon("uzunluk", self._fn_uzunluk, 1)
        self.fonksiyonlar["sayiya_cevir"] = YerlesikFonksiyon("sayiya_cevir", self._fn_sayiya_cevir, 1)
        self.fonksiyonlar["metne_cevir"] = YerlesikFonksiyon("metne_cevir", self._fn_metne_cevir, 1)
        self.fonksiyonlar["tip"] = YerlesikFonksiyon("tip", self._fn_tip, 1)
        self.fonksiyonlar["ekle"] = YerlesikFonksiyon("ekle", self._fn_ekle, 2)
        self.fonksiyonlar["sil"] = YerlesikFonksiyon("sil", self._fn_sil, 2)

    def girdi_ayarla(self, girdiler: List[str]):
        self.girdi_kaynagi = girdiler
        self.girdi_pozisyon = 0

    def _fn_yazdir(self, *args):
        cikti = " ".join(str(a) for a in args)
        self.cikti.append(cikti)
        return None

    def _fn_oku(self):
        if self.girdi_kaynagi:
            if self.girdi_pozisyon < len(self.girdi_kaynagi):
                deger = self.girdi_kaynagi[self.girdi_pozisyon]
                self.girdi_pozisyon += 1
                return deger
            return ""
        return input("> ")

    def _fn_uzunluk(self, deger):
        return len(deger)

    def _fn_sayiya_cevir(self, deger):
        try:
            if '.' in str(deger):
                return float(deger)
            return int(deger)
        except (ValueError, TypeError):
            raise YorumlayiciHata(f"Sayıya çevrilemedi: '{deger}'")

    def _fn_metne_cevir(self, deger):
        return str(deger)

    def _fn_tip(self, deger):
        if isinstance(deger, bool):
            return "mantık"
        if isinstance(deger, int):
            return "tamsayı"
        if isinstance(deger, float):
            return "ondalık"
        if isinstance(deger, str):
            return "metin"
        if isinstance(deger, list):
            return "liste"
        if deger is None:
            return "boş_değer"
        return "bilinmeyen"

    def _fn_ekle(self, liste, eleman):
        if not isinstance(liste, list):
            raise YorumlayiciHata("Sadece listeye ekleme yapılabilir")
        liste.append(eleman)
        return None

    def _fn_sil(self, liste, indeks):
        if not isinstance(liste, list):
            raise YorumlayiciHata("Sadece listeden silme yapılabilir")
        del liste[indeks]
        return None

    # === İFADE DEĞERLENDİRME ===

    def ifade_calistir(self, dugum: ASTDugum, kapsam: Kapsam = None) -> Any:
        if kapsam is None:
            kapsam = self.kuresel_kapsam

        if isinstance(dugum, SayiIfade):
            return dugum.deger

        if isinstance(dugum, MetinIfade):
            return dugum.deger

        if isinstance(dugum, MantikIfade):
            return dugum.deger

        if isinstance(dugum, BosDegerIfade):
            return None

        if isinstance(dugum, TanitlayiciIfade):
            return kapsam.deger_oku(dugum.ad)

        if isinstance(dugum, IkiliIfade):
            return self._ikili_ifade(dugum, kapsam)

        if isinstance(dugum, TekliIfade):
            return self._tekli_ifade(dugum, kapsam)

        if isinstance(dugum, AtamaIfade):
            return self._atama_ifade(dugum, kapsam)

        if isinstance(dugum, FonksiyonCagri):
            return self._fonksiyon_cagri(dugum, kapsam)

        if isinstance(dugum, ListeIfade):
            return [self.ifade_calistir(e, kapsam) for e in dugum.elemanlar]

        if isinstance(dugum, DiziErisim):
            dizi = kapsam.deger_oku(dugum.ad)
            indeks = self.ifade_calistir(dugum.indeks, kapsam)
            return dizi[indeks]

        if isinstance(dugum, NitelikErisim):
            nesne = kapsam.deger_oku(dugum.nesne)
            if isinstance(nesne, dict):
                return nesne.get(dugum.nitelik)
            return getattr(nesne, dugum.nitelik)

        raise YorumlayiciHata(f"Bilinmeyen ifade türü: {type(dugum).__name__}")

    def _ikili_ifade(self, dugum: IkiliIfade, kapsam: Kapsam) -> Any:
        sol = self.ifade_calistir(dugum.sol, kapsam)
        sag = self.ifade_calistir(dugum.sag, kapsam)
        op = dugum.operator

        if op == '+':
            return sol + sag
        if op == '-':
            return sol - sag
        if op == '*':
            return sol * sag
        if op == '/':
            if sag == 0:
                raise YorumlayiciHata("Sıfıra bölme hatası")
            return sol / sag if isinstance(sol, float) or isinstance(sag, float) else sol // sag
        if op == '%':
            return sol % sag
        if op == '==':
            return sol == sag
        if op == '!=':
            return sol != sag
        if op == '<':
            return sol < sag
        if op == '>':
            return sol > sag
        if op == '<=':
            return sol <= sag
        if op == '>=':
            return sol >= sag
        if op == '&&':
            return sol and sag
        if op == '||':
            return sol or sag

        raise YorumlayiciHata(f"Bilinmeyen operatör: '{op}'")

    def _tekli_ifade(self, dugum: TekliIfade, kapsam: Kapsam) -> Any:
        operand = self.ifade_calistir(dugum.operand, kapsam)
        if dugum.operator == '-':
            return -operand
        if dugum.operator == '!':
            return not operand
        raise YorumlayiciHata(f"Bilinmeyen tekli operatör: '{dugum.operator}'")

    def _atama_ifade(self, dugum: AtamaIfade, kapsam: Kapsam) -> Any:
        deger = self.ifade_calistir(dugum.deger, kapsam)

        if dugum.operator == '=':
            kapsam.atama_yap(dugum.ad, deger)
        elif dugum.operator == '+=':
            mevcut = kapsam.deger_oku(dugum.ad)
            kapsam.atama_yap(dugum.ad, mevcut + deger)
        elif dugum.operator == '-=':
            mevcut = kapsam.deger_oku(dugum.ad)
            kapsam.atama_yap(dugum.ad, mevcut - deger)
        elif dugum.operator == '*=':
            mevcut = kapsam.deger_oku(dugum.ad)
            kapsam.atama_yap(dugum.ad, mevcut * deger)
        elif dugum.operator == '/=':
            mevcut = kapsam.deger_oku(dugum.ad)
            kapsam.atama_yap(dugum.ad, mevcut / deger)

        return deger

    def _fonksiyon_cagri(self, dugum: FonksiyonCagri, kapsam: Kapsam) -> Any:
        ad = dugum.ad

        if ad not in self.fonksiyonlar:
            raise YorumlayiciHata(f"Tanımlanmamış fonksiyon: '{ad}'")

        fonk = self.fonksiyonlar[ad]

        # Yerleşik fonksiyon
        if isinstance(fonk, YerlesikFonksiyon):
            arg_degerleri = [self.ifade_calistir(a, kapsam) for a in dugum.argumanlar]
            return fonk.fonk(*arg_degerleri)

        # Kullanıcı tanımlı fonksiyon
        return self._kullanici_fonksiyon_calistir(fonk, dugum.argumanlar, kapsam)

    def _kullanici_fonksiyon_calistir(self, fonk, argumanlar: List[ASTDugum], kapsam: Kapsam):
        yeni_kapsam = Kapsam(ust=kapsam)

        # Argümanları değerlendir
        arg_degerleri = [self.ifade_calistir(a, kapsam) for a in argumanlar]

        # Parametreleri bağla
        for i, (tip, ad) in enumerate(fonk.parametreler):
            if i < len(arg_degerleri):
                yeni_kapsam.atama_yap(ad, arg_degerleri[i], tip)

        try:
            self._deyim_calistir(fonk.govde, yeni_kapsam)
        except DonHatasi as don:
            return don.deger

        return None

    # === DEYİM ÇALIŞTIRMA ===

    def deyim_calistir(self, dugum: ASTDugum, kapsam: Kapsam = None):
        if kapsam is None:
            kapsam = self.kuresel_kapsam
        return self._deyim_calistir(dugum, kapsam)

    def _deyim_calistir(self, dugum: ASTDugum, kapsam: Kapsam):
        if isinstance(dugum, Program):
            for d in dugum.deyimler:
                self._deyim_calistir(d, kapsam)
            return

        if isinstance(dugum, BlokDeyim):
            blok_kapsam = Kapsam(ust=kapsam)
            for d in dugum.deyimler:
                self._deyim_calistir(d, blok_kapsam)
            return

        if isinstance(dugum, IfadeDeyim):
            self.ifade_calistir(dugum.ifade, kapsam)
            return

        if isinstance(dugum, DegiskenTanim):
            deger = None
            if dugum.deger:
                deger = self.ifade_calistir(dugum.deger, kapsam)
            kapsam.atama_yap(dugum.ad, deger, dugum.tip)
            return

        if isinstance(dugum, AtamaIfade):
            self._atama_ifade(dugum, kapsam)
            return

        if isinstance(dugum, EgerDeyim):
            kosul = self.ifade_calistir(dugum.kosul, kapsam)
            if kosul:
                self._deyim_calistir(dugum.sonra, kapsam)
            elif dugum.degilse:
                self._deyim_calistir(dugum.degilse, kapsam)
            return

        if isinstance(dugum, IleDeyim):
            while self.ifade_calistir(dugum.kosul, kapsam):
                try:
                    self._deyim_calistir(dugum.govde, kapsam)
                except DurHatasi:
                    break
                except DevamHatasi:
                    continue
            return

        if isinstance(dugum, ICINDeyim):
            # Başlangıç
            if dugum.baslangic:
                self._deyim_calistir(dugum.baslangic, kapsam)

            while True:
                # Koşul kontrolü
                if dugum.kosul:
                    kosul = self.ifade_calistir(dugum.kosul, kapsam)
                    if not kosul:
                        break

                try:
                    self._deyim_calistir(dugum.govde, kapsam)
                except DurHatasi:
                    break
                except DevamHatasi:
                    pass

                # Artış
                if dugum.artis:
                    self._deyim_calistir(dugum.artis, kapsam)
            return

        if isinstance(dugum, DonDeyim):
            deger = None
            if dugum.deger:
                deger = self.ifade_calistir(dugum.deger, kapsam)
            raise DonHatasi(deger)

        if isinstance(dugum, DurDeyim):
            raise DurHatasi()

        if isinstance(dugum, DevamDeyim):
            raise DevamHatasi()

        if isinstance(dugum, FonksiyonTanim):
            self.fonksiyonlar[dugum.ad] = dugum
            return

        if isinstance(dugum, YazdirDeyim):
            deger = self.ifade_calistir(dugum.deger, kapsam)
            self.cikti.append(str(deger))
            return

        if isinstance(dugum, OkuDeyim):
            if self.girdi_kaynagi:
                if self.girdi_pozisyon < len(self.girdi_kaynagi):
                    deger = self.girdi_kaynagi[self.girdi_pozisyon]
                    self.girdi_pozisyon += 1
                    if dugum.degisken_ad:
                        kapsam.atama_yap(dugum.degisken_ad, deger)
                    return deger
            return ""

        raise YorumlayiciHata(f"Bilinmeyen deyim türü: {type(dugum).__name__}")

    # === PROGRAM ÇALIŞTIRMA ===

    def calistir(self, program: Program) -> List[str]:
        self._deyim_calistir(program, self.kuresel_kapsam)
        return self.cikti
