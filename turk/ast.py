"""
TÜRK Programlama Dili - AST (Soyut Sözdizim Ağacı) Düğümleri
"""

from typing import List, Any, Optional
from enum import Enum


class ASTDugum:
    """Tüm AST düğümlerinin temel sınıfı"""
    pass


# === İFADELER (Expressions) ===

class SayiIfade(ASTDugum):
    def __init__(self, deger: float):
        self.deger = deger

    def __repr__(self):
        return f"SayiIfade({self.deger})"


class MetinIfade(ASTDugum):
    def __init__(self, deger: str):
        self.deger = deger

    def __repr__(self):
        return f"MetinIfade('{self.deger}')"


class MantikIfade(ASTDugum):
    def __init__(self, deger: bool):
        self.deger = deger

    def __repr__(self):
        return f"MantikIfade({self.deger})"


class BosDegerIfade(ASTDugum):
    def __repr__(self):
        return "BosDegerIfade()"


class TanitlayiciIfade(ASTDugum):
    def __init__(self, ad: str):
        self.ad = ad

    def __repr__(self):
        return f"TanitlayiciIfade('{self.ad}')"


class IkiliIfade(ASTDugum):
    """İki operandlı ifade: a + b, x == y vb."""
    def __init__(self, sol: ASTDugum, operator: str, sag: ASTDugum):
        self.sol = sol
        self.operator = operator
        self.sag = sag

    def __repr__(self):
        return f"IkiliIfade({self.sol} {self.operator} {self.sag})"


class TekliIfade(ASTDugum):
    """Tek operandlı ifade: -x, !flag vb."""
    def __init__(self, operator: str, operand: ASTDugum):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"TekliIfade({self.operator}{self.operand})"


class AtamaIfade(ASTDugum):
    def __init__(self, ad: str, deger: ASTDugum, operator: str = "="):
        self.ad = ad
        self.deger = deger
        self.operator = operator

    def __repr__(self):
        return f"AtamaIfade({self.ad} {self.operator} {self.deger})"


class FonksiyonCagri(ASTDugum):
    def __init__(self, ad: str, argumanlar: List[ASTDugum]):
        self.ad = ad
        self.argumanlar = argumanlar

    def __repr__(self):
        return f"FonksiyonCagri({self.ad}({self.argumanlar}))"


class ListeIfade(ASTDugum):
    def __init__(self, elemanlar: List[ASTDugum]):
        self.elemanlar = elemanlar

    def __repr__(self):
        return f"ListeIfade({self.elemanlar})"


class DiziErisim(ASTDugum):
    def __init__(self, ad: str, indeks: ASTDugum):
        self.ad = ad
        self.indeks = indeks

    def __repr__(self):
        return f"DiziErisim({self.ad}[{self.indeks}])"


class NitelikErisim(ASTDugum):
    def __init__(self, nesne: str, nitelik: str):
        self.nesne = nesne
        self.nitelik = nitelik

    def __repr__(self):
        return f"NitelikErisim({self.nesne}.{self.nitelik})"


# === DEYİMLER (Statements) ===

class IfadeDeyim(ASTDugum):
    """Bir ifadeyi deyim olarak sarmalar"""
    def __init__(self, ifade: ASTDugum):
        self.ifade = ifade

    def __repr__(self):
        return f"IfadeDeyim({self.ifade})"


class DegiskenTanim(ASTDugum):
    def __init__(self, tip: str, ad: str, deger: Optional[ASTDugum] = None):
        self.tip = tip
        self.ad = ad
        self.deger = deger

    def __repr__(self):
        return f"DegiskenTanim({self.tip} {self.ad} = {self.deger})"


class BlokDeyim(ASTDugum):
    def __init__(self, deyimler: List[ASTDugum]):
        self.deyimler = deyimler

    def __repr__(self):
        return f"BlokDeyim({self.deyimler})"


class EgerDeyim(ASTDugum):
    def __init__(self, kosul: ASTDugum, sonra: ASTDugum,
                 degilse: Optional[ASTDugum] = None):
        self.kosul = kosul
        self.sonra = sonra
        self.degilse = degilse

    def __repr__(self):
        return f"EgerDeyim(kosul={self.kosul})"


class IleDeyim(ASTDugum):
    """While döngüsü"""
    def __init__(self, kosul: ASTDugum, govde: ASTDugum):
        self.kosul = kosul
        self.govde = govde

    def __repr__(self):
        return f"IleDeyim(kosul={self.kosul})"


class ForDonguDegisken(ASTDugum):
    def __init__(self, tip: Optional[str], ad: str):
        self.tip = tip
        self.ad = ad


class ICINDeyim(ASTDugum):
    """For döngüsü: için (i = 0; i < 10; i++) veya için (eleman in liste)"""
    def __init__(self, baslangic: Optional[ASTDugum], kosul: Optional[ASTDugum],
                 artis: Optional[ASTDugum], govde: ASTDugum):
        self.baslangic = baslangic
        self.kosul = kosul
        self.artis = artis
        self.govde = govde

    def __repr__(self):
        return f"ICINDeyim()"


class DonDeyim(ASTDugum):
    def __init__(self, deger: Optional[ASTDugum] = None):
        self.deger = deger

    def __repr__(self):
        return f"DonDeyim({self.deger})"


class DurDeyim(ASTDugum):
    def __repr__(self):
        return "DurDeyim()"


class DevamDeyim(ASTDugum):
    def __repr__(self):
        return "DevamDeyim()"


class FonksiyonTanim(ASTDugum):
    def __init__(self, donus_tipi: str, ad: str, parametreler: List[tuple],
                 govde: ASTDugum):
        self.donus_tipi = donus_tipi
        self.ad = ad
        self.parametreler = parametreler  # [(tip, ad), ...]
        self.govde = govde

    def __repr__(self):
        return f"FonksiyonTanim({self.ad}({self.parametreler}))"


class YazdirDeyim(ASTDugum):
    def __init__(self, deger: ASTDugum):
        self.deger = deger

    def __repr__(self):
        return f"YazdirDeyim({self.deger})"


class OkuDeyim(ASTDugum):
    def __init__(self, degisken_ad: Optional[str] = None):
        self.degisken_ad = degisken_ad

    def __repr__(self):
        return f"OkuDeyim({self.degisken_ad})"


class Program(ASTDugum):
    """Kök AST düğümü"""
    def __init__(self, deyimler: List[ASTDugum]):
        self.deyimler = deyimler

    def __repr__(self):
        return f"Program({self.deyimler})"
