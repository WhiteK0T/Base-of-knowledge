---
создал заметку: 2026-07-25T03:25:00
author: WhiteK0T
tags:
  - Android
  - Разработка
  - Отладка
  - Сеть
  - HTTP
  - OkHttp
  - Инструменты
Источник:
  - https://t.me/open_source_friend/5782
  - https://github.com/ProxymanApp/atlantis-android
---

# 🌐 atlantis-android — перехват сетевого трафика своего приложения для Proxyman

**atlantis-android** ([github.com/ProxymanApp/atlantis-android](https://github.com/ProxymanApp/atlantis-android)) — **библиотека-компаньон** для [Proxyman](https://proxyman.com), которую разработчик **встраивает в СВОЁ Android-приложение**, чтобы видеть его HTTP/HTTPS-запросы и ответы в десктопном Proxyman **без настройки прокси и без установки сертификатов**. Kotlin, ~445★, v1.0.0. Android-аналог давно существующей iOS-библиотеки Atlantis того же Proxyman.

> [!warning] Главное: это НЕ «сниффер чужих приложений», а dev-инструмент для своего кода
> Формулировка поста «перехват трафика приложений» звучит так, будто можно подслушать любое приложение на телефоне. **Это не так.**
> | Как можно понять | Как на самом деле |
> | :--- | :--- |
> | «перехватывает трафик приложений» | ❌ только **того приложения, в которое ты сам встроил библиотеку** (`debugImplementation` + `Atlantis.getInterceptor()`). Это инструмент разработчика для отладки **собственного** приложения, а не перехват чужого софта |
> | «без прокси и сертификатов — магия» | ✅ но объяснимо: библиотека цепляется **интерцептором внутри HTTP-клиента приложения** (до шифрования TLS), поэтому MITM-сертификат не нужен. Это и есть весь смысл — снять трафик **изнутри** приложения |
> | «любой трафик» | ⚠️ только через **OkHttp** (4.x/5.x): Retrofit 2.9+, Apollo Kotlin 3/4, WebSocket. Если приложение ходит в сеть мимо OkHttp (HttpURLConnection, Ktor c другим движком, нативный код) — **не увидишь** |

> [!caution] Практические ограничения, о которых пост молчит
> - **Нужен Proxyman на десктопе** — а это **коммерческое** приложение (есть бесплатный тариф с лимитами) и **прежде всего под macOS** (README прямо: «Open Proxyman on your **Mac**»; под Windows — бета, полноценного Linux-клиента нет). **Для тебя (Gentoo/Linux) это главный стопор**: сама библиотека опенсорс, но приёмник — платный и не-Linux.
> - **Нет лицензии**: в репозитории **нет файла LICENSE** (GitHub: `None`) — формально «все права защищены», хотя код открыт. Для «просто пользоваться как зависимость» ок, для форка/переиспользования — юридически мутно.
> - **Только debug-сборки**: подключается как `debugImplementation` — в релиз не должно попадать (и правильно: снимать трафик в проде нельзя).
> - **Свежая и подзастывшая**: v1.0.0, последний коммит — **март 2026** (~4 месяца тишины на момент заметки).
> - Требования: **Android 8.0+ (API 26)**, OkHttp 4/5, Kotlin 1.9+; связь с Proxyman по TCP + **NSD/mDNS** (автопоиск в одной сети) или прямое подключение для эмулятора.

## 🛠️ Как подключается (по README)

```kotlin
// build.gradle.kts — только для debug
dependencies { debugImplementation("com.github.ProxymanApp:atlantis-android:v1.0.0") }

// Application.onCreate()
if (BuildConfig.DEBUG) { Atlantis.start(this) }

// OkHttpClient
val client = OkHttpClient.Builder()
    .addInterceptor(Atlantis.getInterceptor())
    .build()
```
Дальше открываешь Proxyman на маке, запускаешь приложение — трафик появляется. WebSocket ловится через `Atlantis.wrapWebSocketListener(...)`. Данные жмутся GZIP.

> [!tip] Если Proxyman-на-маке нет — альтернативы под твой сетап
> - **Chucker** — полностью **опенсорсный** on-device инспектор сети для OkHttp: показывает запросы/ответы **прямо в самом приложении** (уведомление + экран), **без десктопа и без macOS**. Ближайший бесплатный аналог для той же задачи.
> - **mitmproxy** (кроссплатформенный, Linux ок) или Charles — классический подход **через системный прокси + свой CA-сертификат**: ловит трафик любого приложения, но требует установки сертификата и (на свежих Android) правки network-security-config для user-CA. Мощнее по охвату, дороже по настройке.

## 🖥️ Применимость на системах владельца

| Система | Как использовать |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ⚠️ библиотеку собрать/подключить можно (это Gradle-зависимость), но **приёмник Proxyman под Linux фактически недоступен** → на Linux сценарий не закрывается. Реально пригодится, только если есть Mac. Иначе смотри Chucker/mitmproxy |
| **Windows** | 🟡 Proxyman под Windows — бета; может сработать, но не так гладко, как на macOS |
| **Entware / RT-AX56U** | ➖ неактуально: это про разработку Android-приложений на десктопе |

## 🔗 Связанные заметки

- Другой десктопный инструмент отладки Android: [aya — GUI над ADB](aya%20%E2%80%94%20%D0%B4%D0%B5%D1%81%D0%BA%D1%82%D0%BE%D0%BF%D0%BD%D1%8B%D0%B9%20GUI%20%D0%BD%D0%B0%D0%B4%20ADB%20%D0%B4%D0%BB%D1%8F%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20Android%20%28%D0%B7%D0%B5%D1%80%D0%BA%D0%B0%D0%BB%D0%BE%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%2C%20%D1%84%D0%B0%D0%B9%D0%BB%D1%8B%2C%20%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%2C%20%D0%BB%D0%BE%D0%B3%D0%B8%29.md)
- Инструменты Android-разработки (эмуляторы/ADB): [simutil — TUI эмуляторов/ADB](simutil%20%28dungngminh%29%20%E2%80%94%20TUI%20%D0%B4%D0%BB%D1%8F%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0%20Android-%D1%8D%D0%BC%D1%83%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%BE%D0%B2%20%D0%B8%20iOS-%D1%81%D0%B8%D0%BC%D1%83%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%BE%D0%B2%2C%20ADB%20%D0%B8%20%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%D0%BE%D0%B2.md)

## 🔗 Ссылки

- Репозиторий: [github.com/ProxymanApp/atlantis-android](https://github.com/ProxymanApp/atlantis-android) · Приёмник: [proxyman.com](https://proxyman.com)
- Источник новости: [@open_source_friend](https://t.me/open_source_friend/5782)

#Android #Разработка #Отладка #Сеть #HTTP #OkHttp #Инструменты
