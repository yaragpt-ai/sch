# 🇹🇷 TÜRK Programlama Dili

C benzeri sözdizimine sahip, tamamen Türkçe anahtar kelimelerle yazılmış bir programlama dili.

> _"Dennis Ritchie ile birlikte C'nin ruhunu Türkçeye taşıdık."_

## 🚀 Hızlı Başlangıç

### Interpreter ile çalıştır (Python gerekli)
```bash
python -m turk.main examples/merhaba.turk
```

### Compiler ile .exe üret (Python + gcc gerekli)
```bash
python -m turk.compiler examples/merhaba.turk -r
```

## 📖 İki Çalıştırma Yöntemi

TÜRK dilinde yazdığınız kodları iki farklı şekilde çalıştırabilirsiniz:

### Yöntem 1: Interpreter (Yorumlayıcı)

Python üzerinde çalışan yorumlayıcı. Hızlı test ve geliştirme için idealdir.

```bash
python -m turk.main dosya.turk
```

**Avantajları:** Kurulumu kolay, hata ayıklama basit
**Dezavantajları:** Python gerektirir, yavaş çalışır

### Yöntem 2: Compiler (Derleyici) → .exe

TÜRK kodunu önce C'ye, sonra gcc ile native `.exe` dosyasına derler.

```bash
# Adım adım
python -m turk.compiler program.turk          # .c dosyası üret
gcc program.c -o program.exe -lm              # .exe üret
program.exe                                   # Çalıştır

# Tek komutla (derle + çalıştır)
python -m turk.compiler program.turk -r

# Sadece derle, çalıştırma
python -m turk.compiler program.turk -c

# C kodunu ekrana bas
python -m turk.compiler program.turk --stdout
```

**Avantajları:** Python gerektirmez, native hız, bağımsız dağıtım
**Dezavantajları:** gcc kurulu olmalı

## ⚙️ Compiler Nasıl Çalışır?

### Derleme Pipeline'ı

```
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌─────────────┐     ┌─────────┐     ┌──────────┐
│  program    │────▶│  Lexer   │────▶│  Parser  │────▶│ KodUretici  │────▶│  .c     │────▶│  .exe    │
│  .turk      │     │          │     │          │     │ (codegen)   │     │  kodu   │     │  (gcc)   │
└─────────────┘     └──────────┘     └──────────┘     └─────────────┘     └─────────┘     └──────────┘
   TÜRK kodu         Token'lar       AST (ağaç)       C kaynak kodu      C dosyası       Native binary
```

### Adım 1: Lexer — Sözcüksel Çözümleme

Kaynak kodu anlamlı parçalara (token) böler:

```
Girdi:  tamsayı x = 42;

Çıktı:  [TAMSAYI, TANITLAYICI(x), ATAMA(=), TAM_SAYI(42), NOKTALI_VIRGUL(;)]
```

### Adım 2: Parser — Ayrıştırma

Token'lardan bir AST (Soyut Sözdizim Ağacı) oluşturur:

```
DegiskenTanim(
  tip: "tamsayı",
  ad: "x",
  deger: SayiIfade(42)
)
```

### Adım 3: KodUretici — C Kodu Üretimi

AST'yi C koduna çevirir. Her TÜRK yapısının C karşılığı vardır:

| TÜRK | C |
|------|---|
| `tamsayı` | `int` |
| `ondalık` | `double` |
| `metin` | `char*` |
| `eğer (kosul) { ... }` | `if (kosul) { ... }` |
| `ile (kosul) { ... }` | `while (kosul) { ... }` |
| `dön deger;` | `return deger;` |
| `yazdir(x);` | `printf("%d\n", x);` |

### Adım 4: GCC — Makine Kodu Derlemesi

Üretilen C kodu gcc ile native makine koduna derlenir:

```bash
gcc program.c -o program.exe -lm
```

### Tam Örnek: Sıfırdan .exe'ye

**1. TÜRK dosyası yazın (`test.turk`):**
```turk
fonk tamsayı kare(tamsayı n) {
    dön n * n;
}

tamsayı i = 1;
ile (i <= 5) {
    yazdir(i);
    yazdir("^2 =");
    yazdir(kare(i));
    i = i + 1;
}
```

**2. C koduna çevirin:**
```bash
python -m turk.compiler test.turk
```

**3. Üretilen C kodu (`test.c`):**
```c
/* === TÜRK Dili Runtime === */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int kare(int n);

int kare(int n) {
    return (n * n);
}

int main() {
    int i = 1;
    while ((i <= 5)) {
        printf("%d\n", i);
        printf("%s\n", "^2 =");
        printf("%d\n", kare(i));
        i = (i + 1);
    }
    return 0;
}
```

**4. gcc ile derleyin:**
```bash
gcc test.c -o test.exe -lm
```

**5. Çalıştırın (Python'a ihtiyaç YOK):**
```bash
test.exe
```

```
1
^2 =
1
2
^2 =
4
3
^2 =
9
4
^2 =
16
5
^2 =
25
```

### Compiler Komut Seçenekleri

| Seçenek | Açıklama |
|---------|----------|
| `dosya.turk` | Derlenecek TÜRK dosyası |
| `-c`, `--compile` | C kodunu gcc ile derle |
| `-r`, `--run` | Derle ve çalıştır |
| `-o AD`, `--cikti AD` | Çıktı dosya adı |
| `--stdout` | C kodunu ekrana bas |
| `--temizle` | Geçici .c dosyasını sil |

### Gereksinimler

- **Interpreter için:** Python 3.8+
- **Compiler için:** Python 3.8+ + gcc (MINGW, MSYS2, WSL, Linux, macOS)

gcc kurulumu:
- **Windows:** [MSYS2](https://www.msys2.org/) veya [MinGW-w64](https://www.mingw-w64.org/)
- **Linux:** `sudo apt install gcc`
- **macOS:** `xcode-select --install`

## 📝 Dil Özellikleri

### Veri Tipleri

| Türkçe | Açıklama | Örnek |
|--------|----------|-------|
| `tamsayı` | Tam sayı | `tamsayı x = 42;` |
| `ondalık` | Ondalıklı sayı | `ondalık pi = 3.14;` |
| `metin` | Metin (string) | `metin ad = "Ali";` |
| `mantık` | Boolean | `mantık aktif = doğru;` |
| `karakter` | Tek karakter | `karakter harf = 'A';` |
| `liste` | Dizi/Liste | `liste sayilar = [1, 2, 3];` |
| `boş` | Void (dönüş tipi) | `fonk boş selamla() { ... }` |

### Anahtar Kelimeler

| Türkçe | Karşılığı | Açıklama |
|--------|-----------|----------|
| `eğer` | if | Koşul deyimi |
| `değilse` | else | Alternatif koşul |
| `değilse eğer` | else if | Zincirleme koşul |
| `ile` | while | While döngüsü |
| `için` | for | For döngüsü |
| `dön` | return | Değer döndürme |
| `dur` | break | Döngüyü sonlandır |
| `devam` | continue | Sonraki iterasyona geç |
| `fonk` | function | Fonksiyon tanımla |
| `yazdir` | print | Ekrana yazdır |
| `oku` | input | Kullanıcıdan girdi al |
| `doğru` | true | Mantıksal doğru |
| `yanlış` | false | Mantıksal yanlış |
| `boş_değer` | null | Boş değer |

### Operatörler

| Operatör | Açıklama | Örnek |
|----------|----------|-------|
| `+` | Toplama | `a + b` |
| `-` | Çıkarma | `a - b` |
| `*` | Çarpma | `a * b` |
| `/` | Bölme | `a / b` |
| `%` | Mod | `a % b` |
| `==` | Eşitlik | `a == b` |
| `!=` | Eşitsizlik | `a != b` |
| `<` `>` `<=` `>=` | Karşılaştırma | `a < b` |
| `&&` | Mantıksal VE | `a && b` |
| `\|\|` | Mantıksal VEYA | `a \|\| b` |
| `!` | Mantıksal DEĞİL | `!a` |
| `=` | Atama | `a = 5` |
| `+=` `-=` `*=` `/=` | Bileşik atama | `a += 5` |

### Yerleşik Fonksiyonlar

| Fonksiyon | Açıklama | Örnek |
|-----------|----------|-------|
| `yazdir(değer)` | Ekrana yazdır | `yazdir("Merhaba");` |
| `oku()` | Girdi oku | `metin ad = oku();` |
| `uzunluk(değer)` | Uzunluk | `uzunluk("merhaba")` → 7 |
| `sayiya_cevir(değer)` | Sayıya çevir | `sayiya_cevir("42")` → 42 |
| `metne_cevir(değer)` | Metne çevir | `metne_cevir(42)` → "42" |
| `tip(değer)` | Tip adı | `tip(42)` → "tamsayı" |

## 💡 Örnekler

### Merhaba Dünya
```turk
yazdir("Merhaba Dünya!");
```

### Değişkenler ve Koşullar
```turk
tamsayı yas = 18;

eğer (yas >= 18) {
    yazdir("Reşitsiniz");
} değilse {
    yazdir("Reşit değilsiniz");
}
```

### Döngüler
```turk
// While döngüsü
tamsayı i = 0;
ile (i < 10) {
    yazdir(i);
    i = i + 1;
}

// For döngüsü
için (tamsayı j = 0; j < 10; j = j + 1) {
    yazdir(j);
}
```

### Fonksiyonlar
```turk
fonk tamsayı faktoriyel(tamsayı n) {
    eğer (n <= 1) {
        dön 1;
    }
    dön n * faktoriyel(n - 1);
}

yazdir(faktoriyel(5));  // 120
```

### FizzBuzz
```turk
tamsayı sayi = 1;
ile (sayi <= 100) {
    eğer (sayi % 15 == 0) {
        yazdir("FizzBuzz");
    } değilse eğer (sayi % 3 == 0) {
        yazdir("Fizz");
    } değilse eğer (sayi % 5 == 0) {
        yazdir("Buzz");
    } değilse {
        yazdir(sayi);
    }
    sayi = sayi + 1;
}
```

## 🗂️ Proje Yapısı

```
dil/
├── turk/
│   ├── __init__.py        # Paket tanımı
│   ├── lexer.py           # Sözcüksel çözümleyici
│   ├── parser.py          # Ayrıştırıcı (AST oluşturucu)
│   ├── ast.py             # AST düğüm tanımları
│   ├── interpreter.py     # Yorumlayıcı
│   ├── compiler.py        # C kod üretici (codegen)
│   ├── compiler_cli.py    # Compiler CLI aracı
│   └── main.py            # Ana çalıştırıcı (interpreter)
└── examples/
    ├── merhaba.turk        # Merhaba Dünya
    ├── fibonacci.turk      # Fibonacci serisi
    ├── asal_sayi.turk      # Asal sayı bulma
    ├── fizzbuzz.turk       # FizzBuzz
    ├── faktoriyel.turk     # Faktöriyel hesaplama
    └── hesap_makinesi.turk # Hesap makinesi
```

## 🏗️ Mimari

### Interpreter Modu
```
.turk → Lexer → Parser → AST → Interpreter → Çıktı
```

### Compiler Modu
```
.turk → Lexer → Parser → AST → KodUretici → .c → gcc → .exe
```

## 📋 Sınırlamalar

- Dizi elemanlarına atama (`dizi[i] = x`) henüz desteklenmiyor
- Sınıf/yapı tanımları AST düzeyinde mevcut ama yorumlayıcıda tam implemente değil
- Harici modül/import desteği yok

## 🤝 Katkıda Bulunma

Pull request'ler ve issue'lar hoş geldiniz!

## 📜 Lisans

Milli İstihbarat Teşkilatı