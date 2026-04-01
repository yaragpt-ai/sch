"""
TÜRK Programlama Dili - C Kod Üretici (Code Generator)
AST'den C kaynak kodu üretir
"""

from typing import List, Dict, Optional, Tuple
from turk.ast import *


class TipEsleme:
    TURK_TO_C = {
        "tamsayı": "int",
        "ondalık": "double",
        "metin": "char*",
        "mantık": "int",
        "karakter": "char",
        "boş": "void",
    }

    @classmethod
    def c_tipi(cls, turk_tipi: str) -> str:
        return cls.TURK_TO_C.get(turk_tipi, "int")


class KodUretici:
    def __init__(self):
        self.c_satirlar: List[str] = []
        self.prototipler: List[str] = []
        self.girinti = 0
        self.yerel_tipler: Dict[str, str] = {}
        self.parametre_tipler: Dict[str, Dict[str, str]] = {}
        self.fonk_donus_tipleri: Dict[str, str] = {}
        self.kullanilan_runtime: set = set()

    def _gi(self) -> str:
        return "    " * self.girinti

    def _e(self, satir=""):
        self.c_satirlar.append(f"{self._gi()}{satir}")

    def _str_lit(self, s: str) -> str:
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t') + '"'

    def _tip(self, t: str) -> str:
        return TipEsleme.c_tipi(t)

    def _tip_bul(self, ad: str) -> str:
        if ad in self.yerel_tipler:
            return self.yerel_tipler[ad]
        for params in self.parametre_tipler.values():
            if ad in params:
                return params[ad]
        return "tamsayı"

    def _fmt(self, dugum: ASTDugum) -> Tuple[str, str]:
        """(format_specifier, c_expression) döndür"""
        if isinstance(dugum, SayiIfade):
            if isinstance(dugum.deger, float):
                return ("%g", self._ifade(dugum))
            return ("%d", self._ifade(dugum))
        if isinstance(dugum, MetinIfade):
            return ("%s", self._ifade(dugum))
        if isinstance(dugum, MantikIfade):
            return ("%d", "1" if dugum.deger else "0")
        if isinstance(dugum, BosDegerIfade):
            return ("%p", "NULL")
        if isinstance(dugum, TanitlayiciIfade):
            tip = self._tip_bul(dugum.ad)
            if tip == "metin":
                return ("%s", dugum.ad)
            if tip == "ondalık":
                return ("%g", dugum.ad)
            if tip == "karakter":
                return ("%c", dugum.ad)
            return ("%d", dugum.ad)
        if isinstance(dugum, FonksiyonCagri):
            donus = self.fonk_donus_tipleri.get(dugum.ad, "tamsayı")
            if donus == "metin":
                return ("%s", self._ifade(dugum))
            if donus == "ondalık":
                return ("%g", self._ifade(dugum))
            return ("%d", self._ifade(dugum))
        # Varsayılan: sayısal
        return ("%d", self._ifade(dugum))

    def _ifade(self, dugum: ASTDugum) -> str:
        if isinstance(dugum, SayiIfade):
            if isinstance(dugum.deger, float):
                v = dugum.deger
                return f"{v:.1f}" if v == int(v) else str(v)
            return str(dugum.deger)

        if isinstance(dugum, MetinIfade):
            return self._str_lit(dugum.deger)

        if isinstance(dugum, MantikIfade):
            return "1" if dugum.deger else "0"

        if isinstance(dugum, BosDegerIfade):
            return "NULL"

        if isinstance(dugum, TanitlayiciIfade):
            return dugum.ad

        if isinstance(dugum, IkiliIfade):
            s = self._ifade(dugum.sol)
            r = self._ifade(dugum.sag)
            op = dugum.operator
            if op == '&&':
                return f"({s} && {r})"
            if op == '||':
                return f"({s} || {r})"
            return f"({s} {op} {r})"

        if isinstance(dugum, TekliIfade):
            o = self._ifade(dugum.operand)
            if dugum.operator == '!':
                return f"(!{o})"
            return f"(-{o})"

        if isinstance(dugum, AtamaIfade):
            d = self._ifade(dugum.deger)
            if dugum.operator == '=':
                return f"{dugum.ad} = {d}"
            return f"{dugum.ad} {dugum.operator} {d}"

        if isinstance(dugum, FonksiyonCagri):
            return self._cagri(dugum)

        if isinstance(dugum, ListeIfade):
            elems = ", ".join(self._ifade(e) for e in dugum.elemanlar)
            return "{" + elems + "}"

        if isinstance(dugum, DiziErisim):
            return f"{dugum.ad}[{self._ifade(dugum.indeks)}]"

        if isinstance(dugum, NitelikErisim):
            return f"{dugum.nesne}.{dugum.nitelik}"

        return "0"

    def _cagri(self, dugum: FonksiyonCagri) -> str:
        ad = dugum.ad
        args = ", ".join(self._ifade(a) for a in dugum.argumanlar)

        if ad == "yazdir":
            self.kullanilan_runtime.add("yazdir")
            return self._yazdir(dugum.argumanlar)
        if ad == "oku":
            self.kullanilan_runtime.add("oku")
            return "oku()"
        if ad == "uzunluk":
            self.kullanilan_runtime.add("uzunluk")
            return f"uzunluk({args})"
        if ad == "sayiya_cevir":
            self.kullanilan_runtime.add("sayiya_cevir")
            return f"sayiya_cevir({args})"
        if ad == "metne_cevir":
            self.kullanilan_runtime.add("metne_cevir")
            return f"metne_cevir({args})"

        return f"{ad}({args})"

    def _yazdir(self, argumanlar: List[ASTDugum]) -> str:
        if not argumanlar:
            return 'printf("\\n")'
        fmtler = []
        degerler = []
        for a in argumanlar:
            f, v = self._fmt(a)
            fmtler.append(f)
            degerler.append(v)
        fmt_str = " ".join(fmtler) + "\\n"
        if degerler:
            return f'printf("{fmt_str}", {", ".join(degerler)})'
        return f'printf("{fmt_str}")'

    def _deyim(self, dugum: ASTDugum):
        if isinstance(dugum, Program):
            for d in dugum.deyimler:
                self._deyim(d)
            return

        if isinstance(dugum, BlokDeyim):
            self.girinti += 1
            for d in dugum.deyimler:
                self._deyim(d)
            self.girinti -= 1
            return

        if isinstance(dugum, IfadeDeyim):
            self._e(f"{self._ifade(dugum.ifade)};")
            return

        if isinstance(dugum, DegiskenTanim):
            ct = self._tip(dugum.tip)
            ad = dugum.ad
            self.yerel_tipler[ad] = dugum.tip
            if dugum.deger:
                self._e(f"{ct} {ad} = {self._ifade(dugum.deger)};")
            else:
                default = '""' if dugum.tip == "metin" else "0"
                self._e(f"{ct} {ad} = {default};")
            return

        if isinstance(dugum, AtamaIfade):
            self._e(f"{self._ifade(dugum)};")
            return

        if isinstance(dugum, EgerDeyim):
            self._eger(dugum)
            return

        if isinstance(dugum, IleDeyim):
            self._e(f"while ({self._ifade(dugum.kosul)}) {{")
            self._deyim(dugum.govde)
            self._e("}")
            return

        if isinstance(dugum, ICINDeyim):
            bas = self._ifade(dugum.baslangic) if dugum.baslangic else ""
            kos = self._ifade(dugum.kosul) if dugum.kosul else "1"
            art = self._ifade(dugum.artis) if dugum.artis else ""
            self._e(f"for ({bas}; {kos}; {art}) {{")
            self._deyim(dugum.govde)
            self._e("}")
            return

        if isinstance(dugum, DonDeyim):
            if dugum.deger:
                self._e(f"return {self._ifade(dugum.deger)};")
            else:
                self._e("return;")
            return

        if isinstance(dugum, DurDeyim):
            self._e("break;")
            return

        if isinstance(dugum, DevamDeyim):
            self._e("continue;")
            return

        if isinstance(dugum, FonksiyonTanim):
            self._fonk(dugum)
            return

        if isinstance(dugum, YazdirDeyim):
            self._e(f"{self._yazdir([dugum.deger])};")
            return

    def _eger(self, dugum: EgerDeyim, else_if: bool = False):
        kosul = self._ifade(dugum.kosul)
        keyword = "else if" if else_if else "if"
        self._e(f"{keyword} ({kosul}) {{")
        self._deyim(dugum.sonra)
        self._e("}")

        if dugum.degilse:
            if isinstance(dugum.degilse, EgerDeyim):
                self._eger(dugum.degilse, else_if=True)
            else:
                self._e("else {")
                self._deyim(dugum.degilse)
                self._e("}")

    def _fonk(self, dugum: FonksiyonTanim):
        cd = self._tip(dugum.donus_tipi)
        ad = dugum.ad
        self.fonk_donus_tipleri[ad] = dugum.donus_tipi

        pmap = {}
        c_params = []
        for tip, pad in dugum.parametreler:
            ct = self._tip(tip)
            c_params.append(f"{ct} {pad}")
            pmap[pad] = tip
        self.parametre_tipler[ad] = pmap

        ps = ", ".join(c_params) if c_params else "void"
        self.prototipler.append(f"{cd} {ad}({ps});")

        self._e(f"{cd} {ad}({ps}) {{")
        # _deyim BlokDeyim için girinti artıracak
        self._deyim(dugum.govde)
        self._e("}")
        self._e()

    def _runtime(self) -> str:
        r = []
        r.append("/* === TÜRK Dili Runtime === */")
        r.append("#include <stdio.h>")
        r.append("#include <stdlib.h>")
        r.append("#include <string.h>")
        r.append("")

        if "oku" in self.kullanilan_runtime:
            r.append("static char __oku_buf[1024];")
            r.append("char* oku() {")
            r.append("    if (fgets(__oku_buf, sizeof(__oku_buf), stdin)) {")
            r.append("        size_t len = strlen(__oku_buf);")
            r.append("        if (len && __oku_buf[len-1] == '\\n') __oku_buf[len-1] = 0;")
            r.append("    }")
            r.append("    return __oku_buf;")
            r.append("}")
            r.append("")

        if "uzunluk" in self.kullanilan_runtime:
            r.append("int uzunluk(const char* s) { return (int)strlen(s); }")
            r.append("")

        if "sayiya_cevir" in self.kullanilan_runtime:
            r.append("double sayiya_cevir(const char* s) { return atof(s); }")
            r.append("")

        if "metne_cevir" in self.kullanilan_runtime:
            r.append("static char __mtc_buf[64];")
            r.append("char* metne_cevir(double n) {")
            r.append("    if (n == (int)n) sprintf(__mtc_buf, \"%d\", (int)n);")
            r.append("    else sprintf(__mtc_buf, \"%g\", n);")
            r.append("    return __mtc_buf;")
            r.append("}")
            r.append("")

        return "\n".join(r)

    def uret(self, program: Program) -> str:
        # Global ifadeleri topla
        global_deyimler = []
        for d in program.deyimler:
            if isinstance(d, FonksiyonTanim):
                self._fonk(d)
            else:
                global_deyimler.append(d)

        # main fonksiyonu
        main_var = any(
            isinstance(d, FonksiyonTanim) and d.ad == "ana"
            for d in program.deyimler
        )

        if global_deyimler and not main_var:
            self._e("int main() {")
            self.girinti += 1
            for d in global_deyimler:
                self._deyim(d)
            self._e("return 0;")
            self.girinti -= 1
            self._e("}")

        protos = "\n".join(self.prototipler)
        if protos:
            protos += "\n"

        return self._runtime() + "\n" + protos + "\n" + "\n".join(self.c_satirlar)
