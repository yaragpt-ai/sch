"""
TÜRK Programlama Dili - Ayrıştırıcı (Parser)
Token akışından AST (Soyut Sözdizim Ağacı) oluşturur
"""

from typing import List, Optional, Tuple
from turk.lexer import Token, TokenType
from turk.ast import *


class ParserHata(Exception):
    def __init__(self, mesaj: str, satir: int = 0):
        self.mesaj = mesaj
        self.satir = satir
        super().__init__(f"Satır {satir}: {mesaj}")


class Parser:
    def __init__(self, tokenler: List[Token]):
        self.tokenler = tokenler
        self.pozisyon = 0
        self.hatalar: List[str] = []

    def _simdiki(self) -> Token:
        if self.pozisyon >= len(self.tokenler):
            return self.tokenler[-1]  # DOSYA_SONU
        return self.tokenler[self.pozisyon]

    def _ilerle(self) -> Token:
        token = self._simdiki()
        if self.pozisyon < len(self.tokenler) - 1:
            self.pozisyon += 1
        return token

    def _bekle(self, tip: TokenType) -> Token:
        token = self._simdiki()
        if token.tip != tip:
            raise ParserHata(
                f"Beklenen: {tip.name}, bulunan: {token.tip.name} ('{token.deger}')",
                token.satir
            )
        return self._ilerle()

    def _eslesiyor_mu(self, tip: TokenType) -> Optional[Token]:
        if self._simdiki().tip == tip:
            return self._ilerle()
        return None

    def _tip_bak(self, offset: int = 0) -> TokenType:
        idx = self.pozisyon + offset
        if idx >= len(self.tokenler):
            return TokenType.DOSYA_SONU
        return self.tokenler[idx].tip

    def _deger_bak(self, offset: int = 0) -> str:
        idx = self.pozisyon + offset
        if idx >= len(self.tokenler):
            return ""
        return self.tokenler[idx].deger

    def _tip_bak_isim(self, tip: TokenType) -> Optional[str]:
        """Bir sonraki token belirtilen tipteyse değerini döndür, değilse None"""
        if self._simdiki().tip == tip:
            deger = self._simdiki().deger
            self._ilerle()
            return deger
        return None

    def _is_tip(self, *tipler: TokenType) -> bool:
        return self._simdiki().tip in tipler

    def _is_deger(self, deger: str) -> bool:
        return self._simdiki().deger == deger

    # === VERİ TİPLERİ ===

    def _tip_oku(self) -> Optional[str]:
        """Veri tipi oku: tamsayı, ondalık, metin, mantık, karakter, boş"""
        tip_tokenlari = {
            TokenType.TAMSAYI: "tamsayı",
            TokenType.ONDALIK: "ondalık",
            TokenType.METIN: "metin",
            TokenType.MANTIK: "mantık",
            TokenType.KARAKTER: "karakter",
            TokenType.BOŞ: "boş",
            TokenType.LISTE: "liste",
        }
        if self._simdiki().tip in tip_tokenlari:
            tip = tip_tokenlari[self._simdiki().tip]
            self._ilerle()
            return tip
        return None

    # === BİRİNCİL İFADELER ===

    def _birincil(self) -> ASTDugum:
        token = self._simdiki()

        if token.tip == TokenType.TAM_SAYI:
            self._ilerle()
            return SayiIfade(int(token.deger))

        if token.tip == TokenType.ONDALIK_SAYI:
            self._ilerle()
            return SayiIfade(float(token.deger))

        if token.tip == TokenType.METIN_DEGER:
            self._ilerle()
            return MetinIfade(token.deger)

        if token.tip == TokenType.KARAKTER_DEGER:
            self._ilerle()
            return MetinIfade(token.deger)

        if token.tip == TokenType.DOĞRU:
            self._ilerle()
            return MantikIfade(True)

        if token.tip == TokenType.YANLIŞ:
            self._ilerle()
            return MantikIfade(False)

        if token.tip == TokenType.BOŞ_DEĞER:
            self._ilerle()
            return BosDegerIfade()

        if token.tip == TokenType.SOL_PARANTEZ:
            self._ilerle()
            ifade = self._ifade()
            self._bekle(TokenType.SAG_PARANTEZ)
            return ifade

        if token.tip == TokenType.SOL_KOSE:
            return self._liste_oku()

        if token.tip == TokenType.TANITLAYICI:
            return self._tanitlayici_oku()

        if token.tip == TokenType.DEGIL:
            self._ilerle()
            operand = self._birincil()
            return TekliIfade("!", operand)

        if token.tip == TokenType.EKSİ:
            self._ilerle()
            operand = self._birincil()
            return TekliIfade("-", operand)

        raise ParserHata(f"Beklenmeyen token: {token.tip.name} ('{token.deger}')", token.satir)

    def _liste_oku(self) -> ListeIfade:
        self._bekle(TokenType.SOL_KOSE)
        elemanlar = []
        if not self._is_tip(TokenType.SAG_KOSE):
            elemanlar.append(self._ifade())
            while self._eslesiyor_mu(TokenType.VIRGUL):
                elemanlar.append(self._ifade())
        self._bekle(TokenType.SAG_KOSE)
        return ListeIfade(elemanlar)

    def _tanitlayici_oku(self) -> ASTDugum:
        ad = self._simdiki().deger
        self._ilerle()

        # Fonksiyon çağrısı: ad(...)
        if self._is_tip(TokenType.SOL_PARANTEZ):
            self._ilerle()
            argumanlar = []
            if not self._is_tip(TokenType.SAG_PARANTEZ):
                argumanlar.append(self._ifade())
                while self._eslesiyor_mu(TokenType.VIRGUL):
                    argumanlar.append(self._ifade())
            self._bekle(TokenType.SAG_PARANTEZ)
            return FonksiyonCagri(ad, argumanlar)

        # Dizi erişimi: ad[indeks]
        if self._is_tip(TokenType.SOL_KOSE):
            self._ilerle()
            indeks = self._ifade()
            self._bekle(TokenType.SAG_KOSE)
            return DiziErisim(ad, indeks)

        # Nitelik erişimi: ad.nitelik
        if self._is_tip(TokenType.NOKTALI):
            self._ilerle()
            nitelik = self._simdiki().deger
            self._ilerle()
            return NitelikErisim(ad, nitelik)

        return TanitlayiciIfade(ad)

    # === ÇARPMA / BÖLME (yüksek öncelik) ===

    def _carpma(self) -> ASTDugum:
        sol = self._birincil()

        while self._is_tip(TokenType.CARPI, TokenType.BÖLÜ, TokenType.MOD):
            op_token = self._ilerle()
            sag = self._birincil()
            sol = IkiliIfade(sol, op_token.deger, sag)

        return sol

    # === TOPLAMA / ÇIKARMA ===

    def _toplama(self) -> ASTDugum:
        sol = self._carpma()

        while self._is_tip(TokenType.ARTI, TokenType.EKSİ):
            op_token = self._ilerle()
            sag = self._carpma()
            sol = IkiliIfade(sol, op_token.deger, sag)

        return sol

    # === KARŞILAŞTIRMA ===

    def _karsilastirma(self) -> ASTDugum:
        sol = self._toplama()

        while self._is_tip(TokenType.KUCUK, TokenType.BUYUK,
                           TokenType.KUCUK_ESIT, TokenType.BUYUK_ESIT):
            op_token = self._ilerle()
            sag = self._toplama()
            sol = IkiliIfade(sol, op_token.deger, sag)

        return sol

    # === EŞİTLİK ===

    def _esitlik(self) -> ASTDugum:
        sol = self._karsilastirma()

        while self._is_tip(TokenType.ESITTIR, TokenType.DEGILDIR):
            op_token = self._ilerle()
            sag = self._karsilastirma()
            sol = IkiliIfade(sol, op_token.deger, sag)

        return sol

    # === MANTIKSAL VE ===

    def _mantiksal_ve(self) -> ASTDugum:
        sol = self._esitlik()

        while self._is_tip(TokenType.VE):
            self._ilerle()
            sag = self._esitlik()
            sol = IkiliIfade(sol, "&&", sag)

        return sol

    # === MANTIKSAL VEYA ===

    def _mantiksal_veya(self) -> ASTDugum:
        sol = self._mantiksal_ve()

        while self._is_tip(TokenType.VEYA):
            self._ilerle()
            sag = self._mantiksal_ve()
            sol = IkiliIfade(sol, "||", sag)

        return sol

    # === ATAMA ===

    def _atama(self) -> ASTDugum:
        sol = self._mantiksal_veya()

        if isinstance(sol, TanitlayiciIfade) and self._is_tip(
                TokenType.ATAMA, TokenType.ARTIR_AT, TokenType.EKSİ_AT,
                TokenType.CARP_AT, TokenType.BÖL_AT):
            op_token = self._ilerle()
            deger = self._atama()  # Sağ ilişkili
            return AtamaIfade(sol.ad, deger, op_token.deger)

        if isinstance(sol, DiziErisim) and self._is_tip(
                TokenType.ATAMA, TokenType.ARTIR_AT, TokenType.EKSİ_AT,
                TokenType.CARP_AT, TokenType.BÖL_AT):
            op_token = self._ilerle()
            deger = self._atama()
            return AtamaIfade(sol.ad, deger, op_token.deger)

        return sol

    # === GENEL İFADE ===

    def _ifade(self) -> ASTDugum:
        return self._atama()

    # === DEYİMLER ===

    def _deyim(self) -> ASTDugum:
        token = self._simdiki()

        # Değişken tanımı: tip ad = değer;
        tip = self._tip_oku()
        if tip is not None:
            ad_token = self._bekle(TokenType.TANITLAYICI)
            ad = ad_token.deger
            deger = None
            if self._eslesiyor_mu(TokenType.ATAMA):
                deger = self._ifade()
            self._bekle(TokenType.NOKTALI_VIRGUL)
            return DegiskenTanim(tip, ad, deger)

        # Eğer (if)
        if self._eslesiyor_mu(TokenType.EGER):
            return self._eger_oku()

        # Değilse (else) - sadece EğerDeyim içinde işlenir
        if self._is_tip(TokenType.DEGILSE):
            raise ParserHata("'değilse' tek başına kullanılamaz", token.satir)

        # İle (while)
        if self._eslesiyor_mu(TokenType.ILE):
            return self._ile_oku()

        # İçin (for)
        if self._eslesiyor_mu(TokenType.ICIN):
            return self._icin_oku()

        # Dön (return)
        if self._eslesiyor_mu(TokenType.DON):
            deger = None
            if not self._is_tip(TokenType.NOKTALI_VIRGUL):
                deger = self._ifade()
            self._bekle(TokenType.NOKTALI_VIRGUL)
            return DonDeyim(deger)

        # Dur (break)
        if self._eslesiyor_mu(TokenType.DUR):
            self._bekle(TokenType.NOKTALI_VIRGUL)
            return DurDeyim()

        # Devam (continue)
        if self._eslesiyor_mu(TokenType.DEVAM):
            self._bekle(TokenType.NOKTALI_VIRGUL)
            return DevamDeyim()

        # Fonksiyon tanımı: fonk tip ad(parametreler) { ... }
        if self._eslesiyor_mu(TokenType.FONK):
            return self._fonksiyon_oku()

        # Blok: { ... }
        if self._is_tip(TokenType.SOL_KUME):
            return self._blok_oku()

        # Yazdır: yazdir(değer);
        if self._is_tip(TokenType.TANITLAYICI) and self._deger_bak() == "yazdir":
            self._ilerle()
            self._bekle(TokenType.SOL_PARANTEZ)
            deger = self._ifade()
            self._bekle(TokenType.SAG_PARANTEZ)
            self._bekle(TokenType.NOKTALI_VIRGUL)
            return YazdirDeyim(deger)

        # Oku: oku(değişken);
        if self._is_tip(TokenType.TANITLAYICI) and self._deger_bak() == "oku":
            self._ilerle()
            self._bekle(TokenType.SOL_PARANTEZ)
            degisken_ad = self._simdiki().deger
            self._bekle(TokenType.TANITLAYICI)
            self._bekle(TokenType.SAG_PARANTEZ)
            self._bekle(TokenType.NOKTALI_VIRGUL)
            return OkuDeyim(degisken_ad)

        # Genel ifade deyimi
        ifade = self._ifade()
        self._bekle(TokenType.NOKTALI_VIRGUL)
        return IfadeDeyim(ifade)

    def _eger_oku(self) -> EgerDeyim:
        self._bekle(TokenType.SOL_PARANTEZ)
        kosul = self._ifade()
        self._bekle(TokenType.SAG_PARANTEZ)
        sonra = self._deyim()

        degilse = None
        if self._eslesiyor_mu(TokenType.DEGILSE):
            if self._eslesiyor_mu(TokenType.EGER):
                # Zincirleme: değilse eğer
                degilse = self._eger_oku()
            else:
                degilse = self._deyim()

        return EgerDeyim(kosul, sonra, degilse)

    def _ile_oku(self) -> IleDeyim:
        self._bekle(TokenType.SOL_PARANTEZ)
        kosul = self._ifade()
        self._bekle(TokenType.SAG_PARANTEZ)
        govde = self._deyim()
        return IleDeyim(kosul, govde)

    def _icin_oku(self) -> ICINDeyim:
        self._bekle(TokenType.SOL_PARANTEZ)

        # Başlangıç
        baslangic = None
        if not self._is_tip(TokenType.NOKTALI_VIRGUL):
            baslangic = self._ifade()
        self._bekle(TokenType.NOKTALI_VIRGUL)

        # Koşul
        kosul = None
        if not self._is_tip(TokenType.NOKTALI_VIRGUL):
            kosul = self._ifade()
        self._bekle(TokenType.NOKTALI_VIRGUL)

        # Artış
        artis = None
        if not self._is_tip(TokenType.SAG_PARANTEZ):
            artis = self._ifade()
        self._bekle(TokenType.SAG_PARANTEZ)

        govde = self._deyim()
        return ICINDeyim(baslangic, kosul, artis, govde)

    def _fonksiyon_oku(self) -> FonksiyonTanim:
        # Dönüş tipi
        donus_tipi = self._tip_oku() or "boş"

        # Fonksiyon adı
        ad_token = self._bekle(TokenType.TANITLAYICI)
        ad = ad_token.deger

        # Parametreler
        self._bekle(TokenType.SOL_PARANTEZ)
        parametreler: List[Tuple[str, str]] = []
        if not self._is_tip(TokenType.SAG_PARANTEZ):
            tip = self._tip_oku() or "boş"
            ad_p = self._bekle(TokenType.TANITLAYICI).deger
            parametreler.append((tip, ad_p))
            while self._eslesiyor_mu(TokenType.VIRGUL):
                tip = self._tip_oku() or "boş"
                ad_p = self._bekle(TokenType.TANITLAYICI).deger
                parametreler.append((tip, ad_p))
        self._bekle(TokenType.SAG_PARANTEZ)

        # Gövde
        govde = self._blok_oku()

        return FonksiyonTanim(donus_tipi, ad, parametreler, govde)

    def _blok_oku(self) -> BlokDeyim:
        self._bekle(TokenType.SOL_KUME)
        deyimler = []
        while not self._is_tip(TokenType.SAG_KUME) and not self._is_tip(TokenType.DOSYA_SONU):
            deyimler.append(self._deyim())
        self._bekle(TokenType.SAG_KUME)
        return BlokDeyim(deyimler)

    # === PROGRAM ===

    def ayrıştır(self) -> Program:
        deyimler = []
        while not self._is_tip(TokenType.DOSYA_SONU):
            deyimler.append(self._deyim())
        return Program(deyimler)
