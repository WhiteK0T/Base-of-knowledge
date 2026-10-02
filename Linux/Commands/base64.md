---
создал заметку: 2026-10-02T12:30:00
author: WhiteK0T
tags:
  - base64
  - Linux
  - Commands
  - Encoding
  - Шпаргалка
Источник:
  - https://www.gnu.org/software/coreutils/manual/html_node/base64-invocation.html
  - https://www.baeldung.com/linux/cli-base64-encode-decode
---

# 🔤 base64 — шпаргалка

**`base64`** (GNU coreutils) кодирует и декодирует данные в Base64 (алфавит RFC 4648): бинарные данные → безопасный ASCII-текст и обратно. Нужен, чтобы «протащить» бинарь через текстовые каналы (почта/MIME, data-URI, JSON, заголовки, конфиги).

> [!warning] Base64 — это НЕ шифрование
> Это обратимое **кодирование** без ключа: любой декодирует обратно. Не использовать для «скрытия» секретов. Плюс объём растёт **на ~33 %** (3 байта → 4 символа).

---

## ⚙️ Ключи (GNU coreutils)

| Опция | Что делает |
| :--- | :--- |
| *(без опций)* | **кодировать** stdin/FILE в stdout |
| `-d`, `--decode` | **декодировать** |
| `-i`, `--ignore-garbage` | при декодировании игнорировать символы вне алфавита |
| `-w COLS`, `--wrap=COLS` | переносить строку после COLS символов (по умолчанию **76**); **`-w 0`** — одной строкой |
| `--help`, `--version` | справка / версия |

Вход — FILE или stdin (или `-`). При декодировании переносы строк во входе допускаются.

> [!tip] Родственные команды
> `basenc` (coreutils) умеет больше кодировок: `--base64`, **`--base64url`** (URL-safe), `--base32`, `--base16`, `--z85`. А `openssl base64` / `openssl enc -base64` — альтернатива, если coreutils нет.

---

## 🧪 Практика (доп. материал)

**Строка ↔ Base64** (важно `-n`/`printf`, иначе `echo` добавит перевод строки и он попадёт в кодирование):
```bash
printf '%s' 'Hello' | base64            # SGVsbG8=
echo -n 'Hello' | base64                # то же
echo 'SGVsbG8=' | base64 -d             # Hello
base64 <<< 'Hello'                       # here-string (но добавит \n перед кодированием)
```

**Файлы:**
```bash
base64 photo.png > photo.b64            # закодировать файл
base64 -d photo.b64 > photo.png         # раскодировать обратно
base64 -w 0 cert.der                    # одной строкой (для вставки в конфиг/JSON)
```

**URL-safe Base64** (`+/` → `-_`, без `=`): штатный `base64` так не умеет — через `basenc` или `tr`:
```bash
printf '%s' 'data' | basenc --base64url            # кодирование URL-safe
echo 'ZGF0YQ' | basenc -d --base64url              # декодирование
# без basenc — трансляция алфавита:
printf '%s' 'data' | base64 -w0 | tr '+/' '-_' | tr -d '='
```

**Частые кейсы:**
```bash
# Basic Auth заголовок
printf '%s' 'user:pass' | base64                   # dXNlcjpwYXNz

# прочитать payload JWT (вторая часть; JWT использует base64url без '=')
cut -d. -f2 <<< "$JWT" | tr '_-' '/+' | base64 -d 2>/dev/null; echo

# data-URI для картинки
echo "data:image/png;base64,$(base64 -w0 icon.png)"

# проверить округление/битость: длина валидного base64 кратна 4
s='SGVsbG8='; (( ${#s} % 4 == 0 )) && echo "длина ок (кратна 4)" || echo "битая длина"
```

> [!note] GNU vs BSD/macOS
> На macOS/BSD у `base64` другой синтаксис: декодирование часто `-D` (а не `-d`), перенос строк `-b COLS` (а не `-w`), длинных опций нет. В скриптах под оба — проще гнать через `openssl base64 -d`.

---

## 💻 Base64 в языках

### PHP
```php
$enc = base64_encode($data);
$dec = base64_decode($enc);                 // 2-й арг true → строгий режим, false при мусоре
// URL-safe:
$u = rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
$d = base64_decode(strtr($u, '-_', '+/'));
```
Из shell:
```bash
php -r 'echo base64_encode(stream_get_contents(STDIN));' <<< 'Hello'   # кодировать stdin
php -r 'echo base64_decode($argv[1]);' -- 'SGVsbG8='                   # декодировать
```

### Python
```python
import base64
enc = base64.b64encode(b"text").decode()          # 'dGV4dA=='
dec = base64.b64decode(enc)                        # b'text'  (bytes!)
# строки — через encode/decode:
s_enc = base64.b64encode("тест".encode()).decode()
s_dec = base64.b64decode(s_enc).decode()
# URL-safe (алфавит -_):
u = base64.urlsafe_b64encode(b"data").decode()
d = base64.urlsafe_b64decode(u)
```
Из shell (модуль запускается напрямую):
```bash
python3 -m base64 <<< 'Hello, World!'     # SGVsbG8sIFdvcmxkIQo=  (учитывает \n от <<<)
python3 -m base64 -d <<< 'SGVsbG8='        # декодировать
```
> `b64decode(..., validate=True)` бросит ошибку на мусор; по умолчанию невалидные символы молча игнорируются.

### Perl
```perl
use MIME::Base64;                        # core-модуль, ставить не нужно
my $enc  = encode_base64($data);         # по умолчанию перенос каждые 76 + \n в конце
my $enc1 = encode_base64($data, "");     # 2-й арг — конец строки; "" убирает переносы
my $dec  = decode_base64($enc);
# URL-safe (свежие версии MIME::Base64):
use MIME::Base64 qw(encode_base64url decode_base64url);
my $u = encode_base64url($data);
```
Из shell:
```bash
perl -MMIME::Base64 -0777 -ne 'print encode_base64($_, "")' <<< 'Hello'   # кодировать stdin
perl -MMIME::Base64 -ne 'print decode_base64($_)' <<< 'SGVsbG8='          # декодировать
```

### Java (8+)
```java
import java.util.Base64;
import java.nio.charset.StandardCharsets;

String enc = Base64.getEncoder().encodeToString(bytes);
byte[] dec = Base64.getDecoder().decode(enc);
String text = new String(dec, StandardCharsets.UTF_8);

// URL-safe без паддинга и MIME (перенос 76):
String u = Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
String mime = Base64.getMimeEncoder().encodeToString(bytes);
```
Из shell (без компиляции — через JShell, JDK 9+):
```bash
echo 'System.out.println(java.util.Base64.getEncoder().encodeToString("Hello".getBytes()))' | jshell -q -
```
(подробнее про байты/кодировки — [Ключи в Java (JCA)](../../Programming/Java/Crypto/%D0%9A%D0%BB%D1%8E%D1%87%D0%B8%20%D0%B2%20Java%20%28JCA%29%20%E2%80%94%20%D1%87%D1%82%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyFactory%20%D0%B8%20%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyPairGenerator%20%28SPI%2C%20KeySpec%2C%20PEM-DER%2C%20ECC%2C%20%D0%BF%D0%BE%D1%81%D1%82%D0%BA%D0%B2%D0%B0%D0%BD%D1%82%29.md))

### JavaScript
```js
// Node.js:
const enc = Buffer.from('текст', 'utf8').toString('base64');
const dec = Buffer.from(enc, 'base64').toString('utf8');
const url = Buffer.from(data).toString('base64url');   // URL-safe

// Браузер (btoa/atob работают с Latin1 — на Unicode ломаются!):
const enc2 = btoa(String.fromCharCode(...new TextEncoder().encode('тест')));
const dec2 = new TextDecoder().decode(Uint8Array.from(atob(enc2), c => c.charCodeAt(0)));
// Современно (где доступно): Uint8Array.prototype.toBase64() / Uint8Array.fromBase64()
```
Из shell (Node):
```bash
node -e 'process.stdout.write(require("fs").readFileSync(0).toString("base64"))' <<< 'Hello'  # кодировать
node -e 'process.stdout.write(Buffer.from(require("fs").readFileSync(0,"utf8").trim(),"base64").toString())' <<< 'SGVsbG8='
```
> ⚠️ Классическая ошибка: `btoa('тест')` бросает исключение — он не понимает не-Latin1. Для UTF-8 — через `TextEncoder` (выше) или `Buffer` в Node.

### C (OpenSSL — в stdlib base64 нет)
```c
#include <openssl/evp.h>
// кодирование: dst ≥ 4*((len+2)/3)+1 байт
int n = EVP_EncodeBlock((unsigned char*)dst, (const unsigned char*)src, (int)len);
// декодирование:
int m = EVP_DecodeBlock((unsigned char*)out, (const unsigned char*)b64, (int)b64len);
```
Нюанс: `EVP_DecodeBlock` не всегда корректно обрезает хвостовые нули при длине не кратной 3 — для надёжности использовать потоковый `EVP_DecodeInit/Update/Final` или `BIO_f_base64()`.

### C++ (в std base64 тоже нет)
```cpp
// Вариант 1: та же OpenSSL (EVP_*), как в C.
// Вариант 2: заголовочная библиотека cppcodec:
#include <cppcodec/base64_rfc4648.hpp>
std::string enc = cppcodec::base64_rfc4648::encode(data);
std::vector<uint8_t> dec = cppcodec::base64_rfc4648::decode(enc);
```

### Rust (крейт `base64`, API Engine c 0.21)
```rust
use base64::{engine::general_purpose::{STANDARD, URL_SAFE_NO_PAD}, Engine};

let enc = STANDARD.encode(b"text");
let dec: Vec<u8> = STANDARD.decode(&enc)?;
let u = URL_SAFE_NO_PAD.encode(data);       // URL-safe без '='
```
Из shell: для Rust есть `rust-script`/`evcxr`, но это не из коробки.

> С версии **0.21** старые `base64::encode()/decode()` убраны — только через трейт `Engine` (как выше).

> [!note] Компилируемые языки (C / C++ / Rust)
> Готового shell-однострочника у них нет — код нужно собрать. Если нужен именно CLI, «shell-эквивалент» для них — это сам `base64` / `openssl base64` (в начале заметки), а не язык.

---

## 🖥️ По системам владельца

| Система | Инструмент |
| :--- | :--- |
| **Gentoo** (основная) | `sys-apps/coreutils` — `base64` и `basenc` из коробки |
| **Debian / Ubuntu** | `coreutils` (предустановлен) |
| **Arch** | `coreutils` (предустановлен) |
| **Entware / RT-AX56U** | ⚠️ `base64` обычно есть (busybox), но **урезан**: кодирование и `-d`, без `-w`/`basenc`/URL-safe. При нехватке — `opkg install coreutils-base64` / `coreutils-basenc`, либо `openssl base64` |

---

## 🔗 Связанные заметки

- Открытые файлы/конвейеры и просмотр: [lsof](lsof.md)
- Передача данных по сети (часто вместе с base64 в заголовках): [cURL](curl.md)
- Base64 внутри криптозадач (ключи/PEM): [Ключи в Java (JCA)](../../Programming/Java/Crypto/%D0%9A%D0%BB%D1%8E%D1%87%D0%B8%20%D0%B2%20Java%20%28JCA%29%20%E2%80%94%20%D1%87%D1%82%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyFactory%20%D0%B8%20%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyPairGenerator%20%28SPI%2C%20KeySpec%2C%20PEM-DER%2C%20ECC%2C%20%D0%BF%D0%BE%D1%81%D1%82%D0%BA%D0%B2%D0%B0%D0%BD%D1%82%29.md)

## 🔗 Ссылки

- [GNU coreutils — base64](https://www.gnu.org/software/coreutils/manual/html_node/base64-invocation.html)
- [Baeldung — Encode/Decode Base64 (CLI)](https://www.baeldung.com/linux/cli-base64-encode-decode)

#base64 #Linux #Commands #Encoding #Шпаргалка
