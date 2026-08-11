---
создал заметку: 2026-08-11T09:15:00
author: WhiteK0T
tags:
  - Java
  - Криптография
  - JCA
  - KeyFactory
  - KeyPairGenerator
  - Безопасность
  - Программирование
Источник:
  - https://t.me/javatasks/2369
  - https://t.me/javatasks/2371
  - https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/security/KeyFactory.html
  - https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/security/KeyPairGenerator.html
  - https://docs.oracle.com/en/java/javase/25/security/oracle-providers.html
  - https://openjdk.org/jeps/496
  - https://openjdk.org/jeps/470
---

# Ключи в Java (JCA): чтение через `KeyFactory` и генерация через `KeyPairGenerator`

Заметка собрана по двум постам канала `@javatasks` — «Как прочитать криптографический ключ?» ([2369](https://t.me/javatasks/2369)) и «Как создать пару публичный/приватный ключ?» ([2371](https://t.me/javatasks/2371)). Второй пост сам ссылается на первый, темы неразрывные, поэтому здесь они объединены и дополнены **рабочими примерами на актуальных JDK (17 / 21 / 25)**, точными дефолтами провайдеров и разбором граблей, которых в постах нет.

> [!info] Коротко
> - `KeyPairGenerator` — **создаёт** новую пару ключей «из воздуха» (нужен источник случайности).
> - `KeyFactory` — **конвертирует** уже существующий ключ: байты/компоненты ⇄ объект `PublicKey`/`PrivateKey`.
> - Оба — «engine-классы» JCA: реализации подключаются через **SPI-провайдеры**, доступ через `getInstance(алгоритм)`.
> - Это **не** одно и то же и **не** взаимозаменяемо: сгенерировать нельзя «прочитав», прочитать нельзя «сгенерировав».

---

## 1. Архитектура: почему везде `getInstance`

JCA (Java Cryptography Architecture) построена по схеме **engine class + Service Provider Interface**:

```
     твой код                платформа                реализация
  ┌──────────────┐      ┌──────────────────┐      ┌────────────────────┐
  │ KeyFactory   │─────▶│  java.security   │─────▶│ SunRsaSign / SunEC │
  │ .getInstance │      │  Security.getProviders() │ SunJCE / SunPKCS11 │
  │  ("RSA")     │      └──────────────────┘      │ BouncyCastle …     │
  └──────────────┘                                └────────────────────┘
```

- **Engine class** (`KeyFactory`, `KeyPairGenerator`, `Cipher`, `Signature`, `MessageDigest`, `KeyStore`, `SecureRandom`) — публичный, стабильный API. Он **не содержит криптографии**, а только делегирует.
- **SPI-класс** (`KeyFactorySpi`, `KeyPairGeneratorSpi`) — то, что реализует провайдер.
- **Provider** — набор реализаций, зарегистрированный в `java.security` или добавленный в рантайме через `Security.addProvider(...)`.

Поэтому конструктора у этих классов нет — только фабричный `getInstance`. Строка-название алгоритма (`"RSA"`, `"EC"`, `"Ed25519"`, `"ML-KEM"`) — это ключ поиска по зарегистрированным провайдерам.

```java
// 1) любой провайдер, который умеет RSA (в порядке приоритета в java.security)
KeyFactory kf = KeyFactory.getInstance("RSA");

// 2) конкретный провайдер по имени — бросит NoSuchProviderException, если не зарегистрирован
KeyFactory kf2 = KeyFactory.getInstance("RSA", "SunRsaSign");

// 3) конкретный объект-провайдер — регистрировать его в java.security не обязательно
KeyFactory kf3 = KeyFactory.getInstance("RSA", new BouncyCastleProvider());

System.out.println(kf.getProvider().getName()); // SunRsaSign
```

### Штатные провайдеры OpenJDK

| Провайдер | Что даёт (по теме ключей) |
| :--- | :--- |
| `SUN` | `DSA`, `HSS/LMS`, `ML-DSA` (постквантовая подпись, JDK 24+), `SecureRandom` |
| `SunRsaSign` | `RSA`, `RSASSA-PSS` |
| `SunJCE` | `DiffieHellman`, `ML-KEM` (постквантовый KEM, JDK 24+), симметрика |
| `SunEC` | `EC`, `Ed25519`, `Ed448`, `EdDSA`, `X25519`, `X448`, `XDH` |
| `SunPKCS11` | мост к аппаратным токенам/HSM/смарткартам через PKCS#11 (`.so`-модуль) |
| `SunJSSE` / `SunJGSS` / `SunSASL` | TLS и протоколы, не про генерацию ключей напрямую |

> [!tip] Посмотреть, что реально доступно на твоей JVM
> ```java
> for (Provider p : Security.getProviders()) {
>     System.out.println("== " + p.getName() + " " + p.getVersionStr());
>     p.getServices().stream()
>      .filter(s -> s.getType().equals("KeyPairGenerator") || s.getType().equals("KeyFactory"))
>      .sorted(java.util.Comparator.comparing(Provider.Service::getAlgorithm))
>      .forEach(s -> System.out.println("   " + s.getType() + " : " + s.getAlgorithm()));
> }
> ```
> Одной строкой из шелла: `java -XshowSettings:security:providers -version` (JDK 17+).

---

## 2. Иерархия типов ключей

```
                    java.security.Key   (Serializable; getAlgorithm/getFormat/getEncoded)
                     │
        ┌────────────┴────────────┐
   PublicKey                  PrivateKey                    SecretKey  (симметричный, javax.crypto)
        │                          │
   RSAPublicKey               RSAPrivateKey / RSAPrivateCrtKey
   ECPublicKey                ECPrivateKey
   EdECPublicKey              EdECPrivateKey     (Ed25519/Ed448, JDK 15+)
   XECPublicKey               XECPrivateKey      (X25519/X448,  JDK 11+)
   DSAPublicKey               DSAPrivateKey
```

- `KeyPair` — простой контейнер-«кортеж» из `PublicKey` + `PrivateKey`, никакой логики внутри нет (в посте 2371 это сказано верно).
- `AsymmetricKey` (**JDK 22+**) — общий надтип с методом `getParams()`, чтобы доставать параметры (кривую, набор ML-KEM) не приводя к конкретному интерфейсу.
- Три метода `Key`, о которых надо помнить:

| Метод | Что возвращает |
| :--- | :--- |
| `getAlgorithm()` | `"RSA"`, `"EC"`, `"Ed25519"`, … |
| `getFormat()` | `"X.509"` для публичных, `"PKCS#8"` для приватных, **`null`** для ключей внутри HSM/PKCS#11 |
| `getEncoded()` | DER-байты, либо **`null`**, если ключ неэкспортируемый |

> [!warning] `getEncoded()` может вернуть `null`
> Ключ на смарткарте/в HSM физически не покидает устройство. Код вида `Base64.getEncoder().encodeToString(key.getEncoded())` на `SunPKCS11` упадёт с `NullPointerException`. Всегда проверяй `getFormat() != null` перед экспортом.

---

## 3. `KeySpec` — «прозрачное» представление ключа

Ключевая мысль поста 2369: `KeyFactory` конвертирует **спецификацию** ⇄ **ключ**. Терминология из javadoc:

- **Opaque (непрозрачный)** — объект `Key`. Ты не видишь внутренностей, только алгоритм/формат/байты.
- **Transparent (прозрачный)** — объект `KeySpec`. Материал ключа доступен по компонентам.

| `KeySpec` | Что это | Куда |
| :--- | :--- | :--- |
| `X509EncodedKeySpec` | DER `SubjectPublicKeyInfo` (то, что в PEM `-----BEGIN PUBLIC KEY-----`) | **публичный** |
| `PKCS8EncodedKeySpec` | DER `PrivateKeyInfo` (PEM `-----BEGIN PRIVATE KEY-----`) | **приватный** |
| `RSAPublicKeySpec` | модуль `n` + **публичная** экспонента `e` | публичный |
| `RSAPrivateKeySpec` | модуль `n` + приватная экспонента `d` | приватный (минимальный) |
| `RSAPrivateCrtKeySpec` | `n, e, d, p, q, dP, dQ, qInv` — форма CRT | приватный (быстрый, реальный) |
| `ECPublicKeySpec` / `ECPrivateKeySpec` | точка `W` / скаляр `S` + `ECParameterSpec` | EC |
| `EdECPublicKeySpec` / `EdECPrivateKeySpec` | точка/seed + `NamedParameterSpec` | Ed25519/Ed448 |
| `DHPublicKeySpec` / `DHPrivateKeySpec` | `y`/`x` + `p`, `g` | Diffie-Hellman |
| `SecretKeySpec` | «сырые» байты симметричного ключа | ⚠ это **не** для `KeyFactory` (см. §8) |

> [!caution] Уточнение к посту 2369
> В посте пример спецификации звучит как «модуль и экспонента **приватного** ключа RSA». Точнее так:
> - `RSAPublicKeySpec(n, e)` — модуль и **публичная** экспонента → это **публичный** ключ;
> - минимальный приватный — `RSAPrivateKeySpec(n, d)`;
> - но реальные RSA-ключи почти всегда хранятся в **CRT-форме** (`RSAPrivateCrtKeySpec`), потому что расшифровка/подпись по китайской теореме об остатках примерно вчетверо быстрее. `KeyFactory` вернёт тебе `RSAPrivateCrtKey`, если CRT-параметры в ключе есть.

---

## 4. `KeyFactory` — читаем ключи

### 4.1 Публичный ключ из DER/PEM (X.509 SubjectPublicKeyInfo)

```java
import java.security.*;
import java.security.spec.*;
import java.nio.file.*;
import java.util.Base64;

static PublicKey readPublicKeyPem(Path pem, String algorithm) throws Exception {
    String body = Files.readString(pem)
            .replaceAll("-----(BEGIN|END) PUBLIC KEY-----", "")
            .replaceAll("\\s", "");                 // убираем переводы строк
    byte[] der = Base64.getDecoder().decode(body);

    KeyFactory kf = KeyFactory.getInstance(algorithm); // "RSA" / "EC" / "Ed25519"
    return kf.generatePublic(new X509EncodedKeySpec(der));
}
```

### 4.2 Приватный ключ из PKCS#8

```java
static PrivateKey readPrivateKeyPem(Path pem, String algorithm) throws Exception {
    String body = Files.readString(pem)
            .replaceAll("-----(BEGIN|END) PRIVATE KEY-----", "")
            .replaceAll("\\s", "");
    byte[] der = Base64.getDecoder().decode(body);

    PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(der);
    try {
        return KeyFactory.getInstance(algorithm).generatePrivate(spec);
    } finally {
        java.util.Arrays.fill(der, (byte) 0);   // не оставляем материал ключа в куче
    }
}
```

> [!danger] Классические грабли: `InvalidKeySpecException` на «ключе от openssl»
> `PKCS8EncodedKeySpec` понимает **только** PKCS#8 (`-----BEGIN PRIVATE KEY-----`). Он **не** понимает:
> - PKCS#1 — `-----BEGIN RSA PRIVATE KEY-----` (традиционный формат OpenSSL);
> - формат OpenSSH — `-----BEGIN OPENSSH PRIVATE KEY-----` (то, что делает `ssh-keygen` по умолчанию);
> - SEC1 EC — `-----BEGIN EC PRIVATE KEY-----`;
> - зашифрованный PKCS#8 — `-----BEGIN ENCRYPTED PRIVATE KEY-----` (для него нужен `EncryptedPrivateKeyInfo`).
>
> Конвертация в понятный Java формат:
> ```bash
> # PKCS#1 / SEC1 → PKCS#8 (без пароля)
> openssl pkcs8 -topk8 -nocrypt -in legacy.pem -out pkcs8.pem
> # ключ OpenSSH → PKCS#8
> ssh-keygen -p -m PKCS8 -f id_ed25519          # ⚠ перезаписывает файл, сделай копию
> # публичный ключ OpenSSH → X.509 SubjectPublicKeyInfo
> ssh-keygen -e -m PKCS8 -f id_ed25519.pub > pub_x509.pem
> ```

### 4.3 Зашифрованный паролем PKCS#8

```java
import javax.crypto.*;
import javax.crypto.spec.PBEKeySpec;

static PrivateKey readEncryptedPkcs8(byte[] der, char[] password, String alg) throws Exception {
    EncryptedPrivateKeyInfo epki = new EncryptedPrivateKeyInfo(der);
    SecretKeyFactory skf = SecretKeyFactory.getInstance(epki.getAlgName()); // напр. PBEWithHmacSHA256AndAES_256
    Key pbeKey = skf.generateSecret(new PBEKeySpec(password));

    Cipher c = Cipher.getInstance(epki.getAlgName());
    c.init(Cipher.DECRYPT_MODE, pbeKey, epki.getAlgParameters());

    PKCS8EncodedKeySpec spec = epki.getKeySpec(c);            // сразу отдаёт PKCS8EncodedKeySpec
    return KeyFactory.getInstance(alg).generatePrivate(spec);
}
```

### 4.4 Разобрать ключ на компоненты — `getKeySpec`

```java
KeyFactory kf = KeyFactory.getInstance("RSA");

// объект-ключ  →  прозрачные компоненты
RSAPublicKeySpec pubSpec = kf.getKeySpec(publicKey, RSAPublicKeySpec.class);
System.out.println("n битов: " + pubSpec.getModulus().bitLength()); // 3072
System.out.println("e = "      + pubSpec.getPublicExponent());      // 65537

// тот же ключ, но в виде DER-байтов
X509EncodedKeySpec derSpec = kf.getKeySpec(publicKey, X509EncodedKeySpec.class);
```

> [!note] Про сигнатуру `getKeySpec`
> `public <T extends KeySpec> T getKeySpec(Key key, Class<T> keySpec)` — это **учебниковый пример «токена типа» `Class<T>`**: из-за стирания типов метод не может «узнать» `T` сам, поэтому тип передают явным параметром, а метод делает `keySpec.cast(...)`. Разбор этого приёма — в заметке [Java Generics — T, wildcards, PECS, стирание типов](../Generics/Java%20Generics%20%E2%80%94%20%D0%B4%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B8%D0%BA%D0%B8%20%28%D0%BE%D0%B1%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F%29%3A%20T%2C%20wildcards%2C%20PECS%2C%20%D1%81%D1%82%D0%B8%D1%80%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%82%D0%B8%D0%BF%D0%BE%D0%B2%20%E2%80%94%20%D1%81%20%D0%B0%D0%BA%D1%82%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%BC%D0%B8%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80%D0%B0%D0%BC%D0%B8.md).

### 4.5 `translateKey` — «чужой» ключ в свою реализацию

```java
// ключ пришёл от BouncyCastle / из чужой библиотеки / по RMI
PublicKey foreign = someLibrary.getKey();
KeyFactory sun = KeyFactory.getInstance("RSA", "SunRsaSign");
PublicKey trusted = (PublicKey) sun.translateKey(foreign);
```

Зачем: реализация `Cipher`/`Signature` из провайдера X может отказаться работать с объектом ключа из провайдера Y (или сделать это медленно, через сериализацию). `translateKey` перепаковывает ключ в «родной» для фабрики класс. Практически то же самое можно сделать вручную: `getEncoded()` → `X509EncodedKeySpec` → `generatePublic()`.

### 4.6 PEM «из коробки» — JDK 25/26 (preview)

До JDK 25 работа с PEM = ручной strip заголовков + Base64 (см. §4.1) либо BouncyCastle. [JEP 470](https://openjdk.org/jeps/470) добавил в **JDK 25 как preview** штатный API, [JEP 524](https://openjdk.org/jeps/524) продлил его вторым preview в **JDK 26**:

```java
// требуется --enable-preview
import java.security.PEMDecoder;
import java.security.PEMEncoder;

PEMDecoder dec = PEMDecoder.of();
PrivateKey priv = dec.decode(Files.readString(Path.of("key.pem")), PrivateKey.class);
KeyPair    kp   = dec.decode(pemWithBothParts, KeyPair.class);

// зашифрованный паролем PKCS#8 — одной строкой
PrivateKey p2 = PEMDecoder.of().withDecryption(password).decode(encPem, PrivateKey.class);

// обратно в PEM
String out = PEMEncoder.of().encodeToString(priv);
String enc = PEMEncoder.of().withEncryption(password).encodeToString(priv);
```

> [!warning] Границы применимости PEM API
> API покрывает типы из **RFC 7468**: `PUBLIC KEY`, `PRIVATE KEY`, `ENCRYPTED PRIVATE KEY`, `CERTIFICATE`, `X509 CRL`. Legacy-заголовок `BEGIN RSA PRIVATE KEY` (PKCS#1) в RFC 7468 не входит — для него по-прежнему нужен `openssl pkcs8 -topk8` или BouncyCastle. И это **preview**: в проде до финализации не использовать, а собирать/запускать придётся с `--enable-preview` (значит, class-файлы жёстко привязаны к версии JDK).

---

## 5. `KeyPairGenerator` — генерируем пару

Архитектурно — брат-близнец `KeyFactory` (это и подчёркивает пост 2371): те же SPI, тот же `getInstance`. Разница в жизненном цикле:

```
getInstance("RSA")  →  initialize(...)  →  generateKeyPair()  →  generateKeyPair()  →  …
                        ^ опционально              ^ каждый вызов = новая пара
```

### 5.1 Два способа инициализации

Из javadoc — ровно две группы `initialize`:

| Способ | Методы | Когда |
| :--- | :--- | :--- |
| **Алгоритмо-независимый** | `initialize(int keysize)`, `initialize(int keysize, SecureRandom)` | RSA, DSA, DH — размер в битах говорит всё |
| **Алгоритмо-специфичный** | `initialize(AlgorithmParameterSpec)`, `initialize(AlgorithmParameterSpec, SecureRandom)` | EC (нужна кривая), Ed25519/X25519 (нужно имя), DSA с общими параметрами |

Три параметра из поста 2371 (размер, `SecureRandom`, `AlgorithmParameterSpec`) — верно, но важно: **размер и `AlgorithmParameterSpec` взаимоисключающие**, это разные перегрузки, а не три слота одного метода.

### 5.2 RSA

```java
KeyPairGenerator rsa = KeyPairGenerator.getInstance("RSA");
rsa.initialize(3072);                                  // явно, а не «как повезёт»
KeyPair pair = rsa.generateKeyPair();

PublicKey  pub  = pair.getPublic();   // экземпляр RSAPublicKey
PrivateKey priv = pair.getPrivate();  // экземпляр RSAPrivateCrtKey
```

С нестандартной публичной экспонентой:

```java
rsa.initialize(new RSAKeyGenParameterSpec(4096, RSAKeyGenParameterSpec.F4)); // F4 = 65537
```

### 5.3 Эллиптические кривые (EC/ECDSA)

```java
KeyPairGenerator ec = KeyPairGenerator.getInstance("EC");
ec.initialize(new ECGenParameterSpec("secp256r1"));   // = NIST P-256 = prime256v1
KeyPair p256 = ec.generateKeyPair();

ec.initialize(new ECGenParameterSpec("secp384r1"));   // NIST P-384
```

> Имена кривых — те же строки, что понимает `openssl ecparam -list_curves`. `SunEC` в современных JDK поддерживает **только** `secp256r1`, `secp384r1`, `secp521r1` (кучу старых/экзотических кривых выпилили в JDK 16). `secp256k1` (биткойн) — **нет**, нужен BouncyCastle.

### 5.4 Ed25519 / X25519 (современный дефолт)

```java
// подпись (JDK 15+, JEP 339)
KeyPair ed = KeyPairGenerator.getInstance("Ed25519").generateKeyPair();

// то же через общий алгоритм + параметр
KeyPairGenerator eddsa = KeyPairGenerator.getInstance("EdDSA");
eddsa.initialize(NamedParameterSpec.ED25519);

// согласование ключей / ECDH-замена (JDK 11+, JEP 324)
KeyPair x = KeyPairGenerator.getInstance("X25519").generateKeyPair();
```

### 5.5 Постквантовые ML-KEM / ML-DSA (JDK 24+)

```java
// ML-KEM — key encapsulation (замена RSA/DH для обмена ключами), JEP 496
KeyPairGenerator kem = KeyPairGenerator.getInstance("ML-KEM");
kem.initialize(NamedParameterSpec.ML_KEM_768);
KeyPair kemPair = kem.generateKeyPair();

// использование — через новый engine-класс KEM (JDK 21+, JEP 452)
KEM.Encapsulator enc = KEM.getInstance("ML-KEM").newEncapsulator(kemPair.getPublic());
KEM.Encapsulated e = enc.encapsulate();
SecretKey shared = e.key();          // у отправителя
byte[] ciphertext = e.encapsulation();

SecretKey shared2 = KEM.getInstance("ML-KEM")
        .newDecapsulator(kemPair.getPrivate()).decapsulate(ciphertext);  // у получателя

// ML-DSA — постквантовая подпись, JEP 497
KeyPairGenerator dsa = KeyPairGenerator.getInstance("ML-DSA");
dsa.initialize(NamedParameterSpec.ML_DSA_65);
```

> [!info] Что уже есть и чего ещё нет
> - **JDK 24**: API `ML-KEM` и `ML-DSA` (`KeyPairGenerator`, `KeyFactory`, `KEM`, `Signature`).
> - **JDK 26**: подпись JAR-ов через ML-DSA (`jarsigner -sigalg ML-DSA-65`) + HPKE (RFC 9180) через `Cipher` + `HPKEParameterSpec`.
> - **JDK 27** (планово, JEP 527): гибридный постквантовый обмен ключами **в TLS**. То есть до JDK 27 `javax.net.ssl` постквантом сам по себе не пользуется — ML-KEM пока доступен только «руками».

### 5.6 Явный `SecureRandom` и переиспользование генератора

```java
SecureRandom rnd = new SecureRandom();          // на Linux — NativePRNG поверх /dev/urandom

KeyPairGenerator g = KeyPairGenerator.getInstance("EC");
g.initialize(new ECGenParameterSpec("secp384r1"), rnd);

// генератор переиспользуемый: сколько раз вызвал — столько разных пар
List<KeyPair> pairs = IntStream.range(0, 5)
        .mapToObj(i -> g.generateKeyPair())
        .toList();
```

`generateKeyPair()` и `genKeyPair()` функционально идентичны (`genKeyPair` — `final`-обёртка, оставленная для совместимости); используй `generateKeyPair()`.

### 5.7 Дефолты провайдеров — **проверенные значения**

Пост 2371 верно говорит: «каждый провайдер устанавливает свои собственные дефолты». Конкретика для штатных провайдеров OpenJDK:

| Алгоритм | Провайдер | Дефолт в **JDK 17** | Дефолт в **JDK 21 / 25** | Допустимые значения |
| :--- | :--- | :--- | :--- | :--- |
| `RSA`, `RSASSA-PSS` | SunRsaSign | 2048 | **3072** | 512…16384 |
| `DSA` | SUN | 2048 | 2048 | кратно 64 в 512…1024, плюс 2048, 3072 |
| `DiffieHellman` | SunJCE | 3072 | 3072 | кратно 64 в 512…1024, плюс 1536…8192 |
| `EC` | SunEC | 256 | **384** | 256, 384, 521 |
| `Ed25519` / `X25519` | SunEC | 255 | 255 | 255 (фиксировано) |
| `Ed448` / `X448` | SunEC | 448 | 448 | 448 (фиксировано) |
| `ML-KEM` | SunJCE | — | ML-KEM-768 (JDK 24+) | 512 / 768 / 1024 |
| `ML-DSA` | SUN | — | ML-DSA-65 (JDK 24+) | 44 / 65 / 87 |

> [!caution] Дефолты **меняются между версиями JDK** — не полагайся на них
> Между 17 и 21 дефолт RSA вырос 2048 → 3072, а EC 256 → 384 (изменение из [JDK-8282995](https://bugs.openjdk.org/browse/JDK-8282995), приведение к CNSA). Тот же код на разных JDK выдаст ключи разного размера. Javadoc прямым текстом: *«it is recommended to explicitly initialize the KeyPairGenerator instead of relying on provider-specific defaults»*. **Всегда вызывай `initialize(...)` явно.**

---

## 6. Сквозной пример: сгенерировать → сохранить → прочитать → подписать

```java
import java.nio.file.*;
import java.nio.file.attribute.PosixFilePermissions;
import java.security.*;
import java.security.spec.*;
import java.util.Base64;

public class KeyRoundTrip {

    static String toPem(String label, byte[] der) {
        String b64 = Base64.getMimeEncoder(64, "\n".getBytes()).encodeToString(der);
        return "-----BEGIN %s-----\n%s\n-----END %s-----\n".formatted(label, b64, label);
    }

    public static void main(String[] args) throws Exception {
        // ---- 1. генерация -------------------------------------------------
        KeyPairGenerator g = KeyPairGenerator.getInstance("EC");
        g.initialize(new ECGenParameterSpec("secp384r1"), new SecureRandom());
        KeyPair kp = g.generateKeyPair();

        // ---- 2. сохранение ------------------------------------------------
        Files.writeString(Path.of("pub.pem"),  toPem("PUBLIC KEY",  kp.getPublic().getEncoded()));
        Path priv = Path.of("priv.pem");
        Files.writeString(priv, toPem("PRIVATE KEY", kp.getPrivate().getEncoded()));
        Files.setPosixFilePermissions(priv, PosixFilePermissions.fromString("rw-------")); // 0600!

        // ---- 3. чтение обратно через KeyFactory ---------------------------
        KeyFactory kf = KeyFactory.getInstance("EC");
        byte[] pubDer = Base64.getMimeDecoder().decode(
                Files.readString(Path.of("pub.pem"))
                     .replaceAll("-----(BEGIN|END) PUBLIC KEY-----", "").strip());
        PublicKey restored = kf.generatePublic(new X509EncodedKeySpec(pubDer));

        // ---- 4. проверка, что это тот же ключ -----------------------------
        System.out.println("равны: " + restored.equals(kp.getPublic())); // true

        // ---- 5. подпись и верификация -------------------------------------
        byte[] data = "важное сообщение".getBytes(java.nio.charset.StandardCharsets.UTF_8);

        Signature signer = Signature.getInstance("SHA384withECDSA");
        signer.initSign(kp.getPrivate());
        signer.update(data);
        byte[] sig = signer.sign();

        Signature verifier = Signature.getInstance("SHA384withECDSA");
        verifier.initVerify(restored);
        verifier.update(data);
        System.out.println("подпись валидна: " + verifier.verify(sig)); // true
    }
}
```

Проверка совместимости с внешним миром:

```bash
openssl pkey -pubin -in pub.pem -text -noout    # покажет NIST CURVE: P-384
openssl pkey     -in priv.pem -text -noout
```

### Хранить ключи в `KeyStore`, а не в файлах

```java
// PKCS#12 — кроссплатформенный, дефолтный формат KeyStore начиная с JDK 9
KeyStore ks = KeyStore.getInstance("PKCS12");
ks.load(null, null);
ks.setKeyEntry("mykey", kp.getPrivate(), password, new Certificate[]{selfSignedCert});
try (OutputStream os = Files.newOutputStream(Path.of("store.p12"))) {
    ks.store(os, password);
}
```

```bash
# то же самое утилитой из JDK
keytool -genkeypair -alias mykey -keyalg EC -groupname secp384r1 \
        -sigalg SHA384withECDSA -validity 365 \
        -keystore store.p12 -storetype PKCS12
keytool -list -v -keystore store.p12
```

---

## 7. `SecureRandom`: где реально болит

```java
new SecureRandom()                       // ← бери это. На Linux: NativePRNG поверх /dev/urandom
SecureRandom.getInstanceStrong()         // ← «сильный», но может ЗАБЛОКИРОВАТЬСЯ
SecureRandom.getInstance("DRBG")         // NIST SP 800-90A, JDK 9+
```

- `securerandom.strongAlgorithms` в `java.security` по умолчанию — `NativePRNGBlocking:SUN,DRBG:SUN`. На Linux `NativePRNGBlocking` читает **`/dev/random`** и на системе с бедной энтропией (свежий VPS, контейнер, embedded, ранний boot) может подвиснуть на секунды или минуты.
- Классический костыль: `-Djava.security.egd=file:/dev/./urandom` (да, `/./` — обход старого бага, из-за которого строка `file:/dev/urandom` игнорировалась).
- **Нюанс против устаревших советов**: начиная с ядра Linux 5.6 (`getrandom()`) и особенно 5.18 (переписанный RNG) `/dev/random` больше не блокируется после инициализации пула. На современном ядре проблема во многом историческая — но в контейнерах, на embedded и при раннем старте всё ещё выстреливает. `sys-apps/haveged` / `sys-apps/rng-tools` ставить «на всякий случай» современному десктопу не нужно.
- **Не** используй `Random`, `ThreadLocalRandom`, `Math.random()` и `UUID.randomUUID()` как источник криптоматериала. Первые три — не CSPRNG вовсе; `UUID.randomUUID()` внутри использует `SecureRandom`, но отдаёт всего 122 бита и фиксирует 6 бит под версию/вариант.

---

## 8. Факты против хайпа и типичные грабли

> [!danger] Не путать четыре разных класса
> | Класс | Для чего | Тип ключа |
> | :--- | :--- | :--- |
> | `KeyPairGenerator` | **создать** пару | асимметричные |
> | `KeyGenerator` | **создать** симметричный ключ (AES, HmacSHA256) | симметричный |
> | `KeyFactory` | **конвертировать** асимметричный ключ ⇄ spec | асимметричные |
> | `SecretKeyFactory` | конвертировать симметричный ключ / вывести из пароля (PBKDF2) | симметричный |
>
> Пост 2369 говорит про `KeyFactory` — это **только асимметрика**. Для AES-ключа `KeyFactory.getInstance("AES")` бросит `NoSuchAlgorithmException`; там нужен `KeyGenerator` или `new SecretKeySpec(bytes, "AES")`.

**«Больше бит — лучше»** — нет. RSA-4096 генерируется секунды (иногда десятки), подписывает заметно медленнее RSA-3072, а по стойкости примерно равен Ed25519/P-256, которые генерируются за микросекунды. Для нового кода дефолт — **Ed25519** (подпись) и **X25519** (обмен ключами); RSA — только когда его требует контрагент/протокол.

**RSA не шифрует большие данные.** `Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding")` за один вызов возьмёт не больше `размер_ключа − накладные` байт (для 3072 бит и OAEP-SHA256 — около 318 байт). Правильно: гибридная схема (RSA/ECDH шифрует случайный AES-ключ, AES-GCM шифрует данные) или готовый HPKE из JDK 26. И **никогда** `"RSA"` без указания режима — это `RSA/ECB/PKCS1Padding`, уязвимый к Bleichenbacher; в JDK 26 его вообще убрали из обязательных к реализации.

**Экземпляры не потокобезопасны.** Javadoc `KeyFactory` и `KeyPairGenerator` (как и `Cipher`, `Signature`, `MessageDigest`) не даёт гарантий потокобезопасности. Общий статический `KeyFactory` на приложение — источник плавающих багов. Делай локальный экземпляр или `ThreadLocal`. Исключение — `SecureRandom`, он потокобезопасен (ценой синхронизации).

**Приватный ключ — не `String`.** `String` неизменяем, живёт в куче до GC и может попасть в heap dump, логи, `toString()`. Работай с `byte[]`/`char[]` и затирай через `Arrays.fill(buf, (byte) 0)`. У `PrivateKey` есть `destroy()` (из `Destroyable`), но многие реализации бросают `DestroyFailedException` — проверяй `isDestroyed()`.

**«Нужен BouncyCastle»** — в 2026 уже чаще нет. Штатных провайдеров хватает для RSA/EC/EdDSA/X25519/PKCS#8/PKCS#12/ML-KEM/ML-DSA. BouncyCastle реально нужен для: PKCS#1/OpenSSH-парсинга без конвертации, `secp256k1`, CMS/S-MIME, генерации CSR (`PKCS10CertificationRequest`), экзотических кривых и ГОСТ. Помни, что каждый добавленный провайдер — это ещё одна зависимость в цепочке поставок.

**«Нужны Unlimited Strength JCE policy files»** — устаревший совет. Начиная с 8u161 / JDK 9 `crypto.policy=unlimited` стоит по умолчанию, ничего скачивать не надо.

**Ошибка `InvalidKeyException: IOException: algid parse error`** почти всегда означает: скормили `X509EncodedKeySpec` приватный ключ (или наоборот), либо передали PKCS#1 вместо PKCS#8. Проверь заголовок PEM и `key.getFormat()`.

**`key.getEncoded()` возвращает копию** массива при каждом вызове — не кэшируй в цикле и не забывай затирать копии приватного материала.

---

## 9. Применимость по системам

Сами `KeyFactory`/`KeyPairGenerator` — часть `java.base`, они одинаковы на любой ОС. Различается только **как ты получаешь JDK** и где лежит конфиг криптографии.

| Система | Как поставить JDK | Где `java.security` | Нюансы по крипте |
| :--- | :--- | :--- | :--- |
| **Gentoo** (основная) | `emerge dev-java/openjdk` — слоты **8/11/17/21/25**, плюс `27_beta`/`28_alpha` в ~arch. Собирается из исходников; бутстрап через `USE=jbootstrap` (двухстадийная сборка) или `USE=system-bootstrap` (уже установленный JDK) | `/usr/lib64/openjdk-<слот>/conf/security/java.security` | Слота **26 в дереве нет** (Gentoo держит LTS + следующий) → штатный PEM API доступен только как preview в слоте 25. Постквант (ML-KEM/ML-DSA) есть с 25-го слота. PKCS#11-токены: `emerge dev-libs/opensc`, модуль `/usr/lib64/opensc-pkcs11.so` |
| **Debian / Ubuntu** | `apt install openjdk-21-jdk` (в свежих — `openjdk-25-jdk`); Adoptium/Temurin через их apt-репозиторий | `/usr/lib/jvm/java-21-openjdk-amd64/conf/security/java.security` | Переключение — `update-alternatives --config java`. Пакет `ca-certificates-java` пересобирает `cacerts` из системного стора — если пропал доверенный CA, копай туда. PKCS#11: `apt install opensc-pkcs11` |
| **Arch** | `pacman -S jdk-openjdk` (текущий), `jdk21-openjdk`, `jdk17-openjdk`; более свежие — из AUR | `/usr/lib/jvm/java-21-openjdk/conf/security/java.security` | Переключение — `archlinux-java set java-21-openjdk`. Arch обычно первым получает свежий JDK — там раньше всего доступны ML-KEM/ML-DSA и PEM API |
| **Entware** (ASUS RT-AX56U, armv7) | ⚠️ **практичной JVM нет** — полноценного OpenJDK под armv7 в репозитории Entware нет, а 512 МБ RAM / 256 МБ flash под JVM не годятся | — | Криптозадачи на роутере решай нативно: `opkg install openssl-util` (генерация/конвертация ключей), `gnupg`. Java-код держи на хосте, роутер используй как транспорт |

> [!tip] Проверка на любой системе
> ```bash
> java -XshowSettings:security:properties -version 2>&1 | grep -i 'crypto.policy\|strongAlgorithms'
> java -XshowSettings:security:providers  -version 2>&1 | head -40
> ```
> Подробнее про установку и переключение JDK на всех четырёх системах — в заметке [Java — платформа и язык (JVM, JDK/JRE, Gentoo)](../Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md).

---

## 10. Чек-лист

- [ ] Всегда `initialize(...)` явно — не полагаться на дефолт провайдера.
- [ ] Новый код: **Ed25519** для подписи, **X25519** для обмена ключами; RSA ≥ 3072 только если требует протокол.
- [ ] `new SecureRandom()`, не `getInstanceStrong()` без нужды и точно не `Random`.
- [ ] Приватный ключ: `byte[]`/`char[]`, затирание, права `0600`, лучше — `KeyStore` PKCS#12.
- [ ] Публичный ключ → `X509EncodedKeySpec`, приватный → `PKCS8EncodedKeySpec`. Не перепутать.
- [ ] Ключ от `openssl`/`ssh-keygen` — сначала `openssl pkcs8 -topk8`, потом в Java.
- [ ] Экземпляры engine-классов — не шарить между потоками.
- [ ] Никогда `Cipher.getInstance("RSA")` без явного режима и паддинга.
- [ ] Проверять `getFormat() != null` перед `getEncoded()` (HSM/PKCS#11).

---

## Связанные заметки

- [Java — платформа и язык (JVM, JDK/JRE, Gentoo)](../Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md) — установка и переключение JDK (Gentoo `eselect java-vm`, слоты, LTS).
- [Java Generics — T, wildcards, PECS, стирание типов](../Generics/Java%20Generics%20%E2%80%94%20%D0%B4%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B8%D0%BA%D0%B8%20%28%D0%BE%D0%B1%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F%29%3A%20T%2C%20wildcards%2C%20PECS%2C%20%D1%81%D1%82%D0%B8%D1%80%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%82%D0%B8%D0%BF%D0%BE%D0%B2%20%E2%80%94%20%D1%81%20%D0%B0%D0%BA%D1%82%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%BC%D0%B8%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80%D0%B0%D0%BC%D0%B8.md) — приём `Class<T>` как «токена типа», который используется в `getKeySpec(Key, Class<T>)`.
- [SSH-Ключи](../../../Network/SSH/SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md) — те же пары ключей с практической стороны: `ssh-keygen`, форматы, `authorized_keys`.
- [Let's Encrypt — выпуск TLS-сертификата](../../../Network/WebServers/Let%27s%20Encrypt%20%E2%80%94%20%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%20TLS-%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%20nginx%20%D0%B8%20Apache%20%28certbot%2C%20acme.sh%2C%20HTTP-01-DNS-01%2C%20wildcard%2C%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BF%D1%80%D0%BE%D0%B4%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md) — X.509-сертификаты, PEM и приватные ключи в связке с TLS.
- [LUKSbox — шифроконтейнер на Rust (постквант ML-KEM)](../../../Security/LUKSbox%20%28PentHertz%29%20%E2%80%94%20%D0%BA%D1%80%D0%BE%D1%81%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20%D1%88%D0%B8%D1%84%D1%80%D0%BE%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%20%D0%BD%D0%B0%20Rust%20%28FIDO2%2C%20TPM%2C%20%D0%BF%D0%BE%D1%81%D1%82%D0%BA%D0%B2%D0%B0%D0%BD%D1%82%20ML-KEM%29%2C%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%20%C2%ABpre-1.0%C2%BB.md) — постквантовый ML-KEM в прикладном инструменте (не в Java).
- [git-crypt — прозрачное шифрование файлов в репозитории](../../../VCS/Git/git-crypt%20%E2%80%94%20%D0%BF%D1%80%D0%BE%D0%B7%D1%80%D0%B0%D1%87%D0%BD%D0%BE%D0%B5%20%D1%88%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B8.md) — GPG-ключи и прозрачное шифрование в репозитории.

## Ссылки

- Посты-источники: [@javatasks/2369 — «Как прочитать криптографический ключ?»](https://t.me/javatasks/2369), [@javatasks/2371 — «Как создать пару публичный/приватный ключ?»](https://t.me/javatasks/2371)
- [Javadoc `KeyFactory` (JDK 25)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/security/KeyFactory.html)
- [Javadoc `KeyPairGenerator` (JDK 25)](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/security/KeyPairGenerator.html)
- [JDK Providers Documentation — таблицы алгоритмов и дефолтных размеров ключей](https://docs.oracle.com/en/java/javase/25/security/oracle-providers.html)
- [Java Security Standard Algorithm Names](https://docs.oracle.com/en/java/javase/25/docs/specs/security/standard-names.html)
- [JEP 324: Key Agreement with Curve25519 and Curve448 (JDK 11)](https://openjdk.org/jeps/324)
- [JEP 339: Edwards-Curve Digital Signature Algorithm (JDK 15)](https://openjdk.org/jeps/339)
- [JEP 496: Quantum-Resistant ML-KEM (JDK 24)](https://openjdk.org/jeps/496) · [JEP 497: Quantum-Resistant ML-DSA (JDK 24)](https://openjdk.org/jeps/497)
- [JEP 470: PEM Encodings (Preview, JDK 25)](https://openjdk.org/jeps/470) · [JEP 524: PEM Encodings (Second Preview, JDK 26)](https://openjdk.org/jeps/524)
- [Sean Mullan — JDK 25 Security Enhancements](https://seanjmullan.org/blog/2025/09/23/jdk25) · [JDK 26 Security Enhancements](https://seanjmullan.org/blog/2026/03/16/jdk26)
- [Gentoo: dev-java/openjdk](https://packages.gentoo.org/packages/dev-java/openjdk)

#Java #Криптография #JCA #KeyFactory #KeyPairGenerator #Безопасность #Программирование
