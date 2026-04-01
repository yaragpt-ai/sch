# 🇹🇷 TÜRK Programlama Dili

C benzeri sözdizimine sahip, tamamen Türkçe anahtar kelimelerle yazılmış bir programlama dili.

> _"Dennis Ritchie ile birlikte C'nin ruhunu Türkçeye taşıdık."_

## 🚀 Kurulum

```bash
# Python 3.8+ gerekli
python -m turk.main examples/merhaba.turk
```

## 📖 Kullanım

### Dosya çalıştırma
```bash
python -m turk.main dosya.turk
```

### Etkileşimli mod
```bash
python -m turk.main
```

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
| `ekle(liste, eleman)` | Listeye ekle | `ekle(liste, 5)` |
| `sil(liste, indeks)` | Listeden sil | `sil(liste, 0)` |

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
│   ├── __init__.py       # Paket tanımı
│   ├── lexer.py          # Sözcüksel çözümleyici
│   ├── parser.py         # Ayrıştırıcı (AST oluşturucu)
│   ├── ast.py            # AST düğüm tanımları
│   ├── interpreter.py    # Yorumlayıcı
│   └── main.py           # Ana çalıştırıcı
└── examples/
    ├── merhaba.turk       # Merhaba Dünya
    ├── fibonacci.turk     # Fibonacci serisi
    ├── asal_sayi.turk     # Asal sayı bulma
    ├── fizzbuzz.turk      # FizzBuzz
    ├── faktoriyel.turk    # Faktöriyel hesaplama
    └── hesap_makinesi.turk # Hesap makinesi
```

## 🏗️ Mimari

TÜRK dili klasik interpreter mimarisi kullanır:

1. **Lexer** → Kaynak kodu token'lara böler
2. **Parser** → Token'lardan AST (Soyut Sözdizim Ağacı) oluşturur
3. **Interpreter** → AST'yi çalıştırır

## 📋 Sınırlamalar

- Şu an için sadece yorumlayıcı (interpreter) mevcut, derleyici yok
- Dizi elemanlarına atama (`dizi[i] = x`) henüz desteklenmiyor
- Sınıf/yapı tanımları AST düzeyinde mevcut ama henüz yorumlayıcıda tam implemente değil
- Harici modül/import desteği yok

## 🤝 Katkıda Bulunma

Pull request'ler ve issue'lar hoş geldiniz!

## 📜 Lisans

Milli İstihbarat Teşkilatı
