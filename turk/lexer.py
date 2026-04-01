"""
TÜRK Programlama Dili - Sözcüksel Çözümleyici (Lexer)
C benzeri Türkçe programlama dili için token üretici
"""

from enum import Enum, auto
from typing import List, Tuple


class TokenType(Enum):
    # Anahtar kelimeler
    EGER = auto()      # if
    DEGILSE = auto()   # else
    DEGILSE_EGER = auto()  # else if
    ILE = auto()       # while
    ICIN = auto()      # for
    DON = auto()       # return
    YAP = auto()       # do
    DUR = auto()       # break
    DEVAM = auto()     # continue
    FONK = auto()      # function
    YAPI = auto()      # struct
    SINIF = auto()     # class
    DENEME = auto()    # try
    YAKALA = auto()    # catch
    AT = auto()        # throw
    OZEL = auto()      # private
    HERKES = auto()    # public
    YAVAŞ = auto()     # protected
    STATIK = auto()    # static
    SABIT = auto()     # const
    BOŞ = auto()       # void
    DOĞRU = auto()     # true
    YANLIŞ = auto()    # false
    BOŞ_DEĞER = auto() # null

    # Veri tipleri
    TAMSAYI = auto()   # int
    ONDALIK = auto()   # float
    METIN = auto()     # string
    MANTIK = auto()    # bool
    KARAKTER = auto()  # char
    LISTE = auto()     # list

    # Operatörler
    ARTI = auto()      # +
    EKSİ = auto()      # -
    CARPI = auto()     # *
    BÖLÜ = auto()      # /
    MOD = auto()       # %
    ARTIR = auto()     # ++
    AZALT = auto()     # --

    ATAMA = auto()     # =
    ARTIR_AT = auto()  # +=
    EKSİ_AT = auto()   # -=
    CARP_AT = auto()   # *=
    BÖL_AT = auto()    # /=

    ESITTIR = auto()   # ==
    DEGILDIR = auto()  # !=
    KUCUK = auto()     # <
    BUYUK = auto()     # >
    KUCUK_ESIT = auto()  # <=
    BUYUK_ESIT = auto()  # >=

    VE = auto()        # &&
    VEYA = auto()      # ||
    DEGIL = auto()     # !

    # Ayırıcılar
    SOL_PARANTEZ = auto()   # (
    SAG_PARANTEZ = auto()   # )
    SOL_KOSE = auto()       # [
    SAG_KOSE = auto()       # ]
    SOL_KUME = auto()       # {
    SAG_KUME = auto()       # }

    VIRGUL = auto()    # ,
    NOKTALI = auto()   # .
    NOKTALI_VIRGUL = auto()  # ;
    İKILI_NOKTA = auto()  # :

    # Değerler
    TAM_SAYI = auto()  # 123
    ONDALIK_SAYI = auto()  # 3.14
    METIN_DEGER = auto()  # "merhaba"
    KARAKTER_DEGER = auto()  # 'a'
    TANITLAYICI = auto()  # değişken adı

    # Özel
    DOSYA_SONU = auto()  # EOF


class Token:
    def __init__(self, tip: TokenType, deger: str = None, satir: int = 0, sutun: int = 0):
        self.tip = tip
        self.deger = deger if deger is not None else tip.name.lower()
        self.satir = satir
        self.sutun = sutun

    def __repr__(self):
        return f"Token({self.tip.name}, '{self.deger}', satir={self.satir})"


# Anahtar kelime haritası
ANAHTAR_KELIMELER = {
    "eğer": TokenType.EGER,
    "değilse": TokenType.DEGILSE,
    "değilse_eğer": TokenType.DEGILSE_EGER,
    "ile": TokenType.ILE,
    "için": TokenType.ICIN,
    "dön": TokenType.DON,
    "yap": TokenType.YAP,
    "dur": TokenType.DUR,
    "devam": TokenType.DEVAM,
    "fonk": TokenType.FONK,
    "yapı": TokenType.YAPI,
    "sınıf": TokenType.SINIF,
    "deneme": TokenType.DENEME,
    "yakala": TokenType.YAKALA,
    "at": TokenType.AT,
    "özel": TokenType.OZEL,
    "herkes": TokenType.HERKES,
    "yavaş": TokenType.YAVAŞ,
    "statik": TokenType.STATIK,
    "sabit": TokenType.SABIT,
    "boş": TokenType.BOŞ,
    "doğru": TokenType.DOĞRU,
    "yanlış": TokenType.YANLIŞ,
    "boş_değer": TokenType.BOŞ_DEĞER,
    "tamsayı": TokenType.TAMSAYI,
    "ondalık": TokenType.ONDALIK,
    "metin": TokenType.METIN,
    "mantık": TokenType.MANTIK,
    "karakter": TokenType.KARAKTER,
    "liste": TokenType.LISTE,
    "ve": TokenType.VE,
    "veya": TokenType.VEYA,
    "değil": TokenType.DEGIL,
}


class Lexer:
    def __init__(self, kaynak: str):
        self.kaynak = kaynak
        self.pozisyon = 0
        self.satir = 1
        self.sutun = 1
        self.tokenler: List[Token] = []
        self.hatalar: List[str] = []

    def _simdiki(self) -> str:
        if self.pozisyon >= len(self.kaynak):
            return '\0'
        return self.kaynak[self.pozisyon]

    def _ileri(self, miktar: int = 1) -> str:
        karakter = ""
        for _ in range(miktar):
            if self.pozisyon < len(self.kaynak):
                karakter = self.kaynak[self.pozisyon]
                if karakter == '\n':
                    self.satir += 1
                    self.sutun = 1
                else:
                    self.sutun += 1
                self.pozisyon += 1
        return karakter

    def _ileri_bak(self, miktar: int = 1) -> str:
        poz = self.pozisyon + miktar
        if poz >= len(self.kaynak):
            return '\0'
        return self.kaynak[poz]

    def _bosluk_atla(self):
        while self._simdiki() in ' \t\r\n':
            self._ileri()

    def _yorum_atla(self):
        if self._simdiki() == '/' and self._ileri_bak() == '/':
            # Tek satırlık yorum
            while self._simdiki() != '\n' and self._simdiki() != '\0':
                self._ileri()
            return True
        elif self._simdiki() == '/' and self._ileri_bak() == '*':
            # Çok satırlı yorum
            self._ileri(2)
            while not (self._simdiki() == '*' and self._ileri_bak() == '/'):
                if self._simdiki() == '\0':
                    self.hatalar.append(f"Satır {self.satir}: Kapanan yorum bulunamadı")
                    return True
                self._ileri()
            self._ileri(2)
            return True
        return False

    def _sayi_oku(self) -> Token:
        baslangic = self.pozisyon
        baslangic_sutun = self.sutun
        ondalik_var = False

        while self._simdiki().isdigit() or (self._simdiki() == '.' and not ondalik_var):
            if self._simdiki() == '.':
                ondalik_var = True
            self._ileri()

        deger = self.kaynak[baslangic:self.pozisyon]
        if ondalik_var:
            return Token(TokenType.ONDALIK_SAYI, deger, self.satir, baslangic_sutun)
        return Token(TokenType.TAM_SAYI, deger, self.satir, baslangic_sutun)

    def _tanitlayici_oku(self) -> Token:
        baslangic = self.pozisyon
        baslangic_sutun = self.sutun

        while self._simdiki().isalnum() or self._simdiki() == '_':
            self._ileri()

        deger = self.kaynak[baslangic:self.pozisyon]

        # Anahtar kelime kontrolü
        if deger in ANAHTAR_KELIMELER:
            return Token(ANAHTAR_KELIMELER[deger], deger, self.satir, baslangic_sutun)

        return Token(TokenType.TANITLAYICI, deger, self.satir, baslangic_sutun)

    def _metin_oku(self) -> Token:
        baslangic_sutun = self.sutun
        alinti = self._simdiki()  # " veya '
        self._ileri()
        deger = ""

        while self._simdiki() != alinti and self._simdiki() != '\0':
            if self._simdiki() == '\\':
                self._ileri()
                kacis = self._simdiki()
                if kacis == 'n':
                    deger += '\n'
                elif kacis == 't':
                    deger += '\t'
                elif kacis == '\\':
                    deger += '\\'
                elif kacis == alinti:
                    deger += alinti
                else:
                    deger += '\\' + kacis
            else:
                deger += self._simdiki()
            self._ileri()

        if self._simdiki() == '\0':
            self.hatalar.append(f"Satır {self.satir}: Kapanan alıntı işareti bulunamadı")

        self._ileri()  # Kapanan alıntıyı atla

        if alinti == '"':
            return Token(TokenType.METIN_DEGER, deger, self.satir, baslangic_sutun)
        return Token(TokenType.KARAKTER_DEGER, deger, self.satir, baslangic_sutun)

    def analiz(self) -> List[Token]:
        while self.pozisyon < len(self.kaynak):
            # Yorumları atla
            if self._yorum_atla():
                continue

            # Boşlukları atla
            self._bosluk_atla()

            if self.pozisyon >= len(self.kaynak):
                break

            karakter = self._simdiki()
            baslangic_sutun = self.sutun

            # Sayılar
            if karakter.isdigit():
                self.tokenler.append(self._sayi_oku())
                continue

            # Tanıtlayıcılar ve anahtar kelimeler
            if karakter.isalpha() or karakter == '_':
                self.tokenler.append(self._tanitlayici_oku())
                continue

            # Metin ve karakter değerleri
            if karakter in '"\'':
                self.tokenler.append(self._metin_oku())
                continue

            # İki karakterli operatörler
            iki_karakter = karakter + self._ileri_bak()

            if iki_karakter == '++':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.ARTIR, '++', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '--':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.AZALT, '--', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '==':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.ESITTIR, '==', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '!=':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.DEGILDIR, '!=', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '<=':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.KUCUK_ESIT, '<=', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '>=':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.BUYUK_ESIT, '>=', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '&&':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.VE, '&&', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '||':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.VEYA, '||', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '+=':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.ARTIR_AT, '+=', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '-=':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.EKSİ_AT, '-=', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '*=':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.CARP_AT, '*=', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '/=':
                self._ileri(2)
                self.tokenler.append(Token(TokenType.BÖL_AT, '/=', self.satir, baslangic_sutun))
                continue
            elif iki_karakter == '//':
                continue  # Yorum zaten işlendi
            elif iki_karakter == '/*':
                continue  # Yorum zaten işlendi

            # Tek karakterli operatörler
            tek_operatörler = {
                '+': TokenType.ARTI,
                '-': TokenType.EKSİ,
                '*': TokenType.CARPI,
                '/': TokenType.BÖLÜ,
                '%': TokenType.MOD,
                '=': TokenType.ATAMA,
                '<': TokenType.KUCUK,
                '>': TokenType.BUYUK,
                '!': TokenType.DEGIL,
                '(': TokenType.SOL_PARANTEZ,
                ')': TokenType.SAG_PARANTEZ,
                '[': TokenType.SOL_KOSE,
                ']': TokenType.SAG_KOSE,
                '{': TokenType.SOL_KUME,
                '}': TokenType.SAG_KUME,
                ',': TokenType.VIRGUL,
                '.': TokenType.NOKTALI,
                ';': TokenType.NOKTALI_VIRGUL,
                ':': TokenType.İKILI_NOKTA,
            }

            if karakter in tek_operatörler:
                self._ileri()
                self.tokenler.append(Token(tek_operatörler[karakter], karakter, self.satir, baslangic_sutun))
                continue

            # Bilinmeyen karakter
            self.hatalar.append(f"Satır {self.satir}, Sütun {baslangic_sutun}: Bilinmeyen karakter '{karakter}'")
            self._ileri()

        # Dosya sonu tokeni
        self.tokenler.append(Token(TokenType.DOSYA_SONU, "DOSYA_SONU", self.satir, self.sutun))
        return self.tokenler
