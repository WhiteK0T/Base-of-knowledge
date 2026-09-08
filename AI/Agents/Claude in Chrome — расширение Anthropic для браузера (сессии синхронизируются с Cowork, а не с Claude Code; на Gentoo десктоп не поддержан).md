---
создал заметку: 2026-09-09T02:50:00
author: WhiteK0T
tags:
  - AI
  - Claude
  - Anthropic
  - Браузер
  - Расширения
  - Безопасность
  - Приватность
Источник:
  - https://t.me/bugnotfeature/27032
  - https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn
  - https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome
  - https://support.claude.com/en/articles/12902428
  - https://code.claude.com/docs/en/desktop-linux
---

# 🌐 Claude in Chrome — расширение Anthropic для браузера

Разбор [поста «Не баг, а фича» от 12.08.2026](https://t.me/bugnotfeature/27032). Расширение настоящее и официальное, но пост подаёт обновление как запуск и путает два разных продукта Anthropic.

Проверено 09.09.2026 по странице в Chrome Web Store, справке Anthropic и документации Claude Code.

> [!info] Факты о расширении
> | | |
> | :--- | :--- |
> | ID / издатель | `fcoeoabgfenejglbffodgkkbkcdhcgfn`, **Anthropic** (издатель подтверждён, нарушений нет) |
> | Пользователей | **15 000 000** |
> | Рейтинг | **2,8** из 5 при 1,6 тыс. оценок |
> | Версия / обновлено | 1.0.91, **04.09.2026** |
> | Размер / язык | 6,44 МиБ, только английский |
> | Доступ | **все платные тарифы** (Pro, Max, Team, Enterprise); бесплатного нет |

## ✅ Проверка утверждений поста

| Утверждение | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «Anthropic **дропнула** расширение» | ❌ Это не запуск | Бета для Max — ноябрь 2025, для всех платных — конец декабря 2025. Расширению около **девяти месяцев**, пост описывает очередное обновление |
| «Сессии между **Claude Code** и Chrome синхронизируются» | ❌ Продукт перепутан | Синхронизируются сессии **Claude Cowork**: боковая панель ↔ веб ↔ Claude Desktop ↔ мобильное приложение. Claude Code интегрирован иначе — как цикл «собрал в терминале → проверил в браузере» |
| «Начать в мобильном приложении и продолжить в браузере» | ✅ Верно | Справка: *«Start a session in the side panel and pick it up on the web, in Claude Desktop, or on Claude Mobile. Sessions live with your Claude account rather than with the machine you started on»* |
| «Скиллы и connectors подключаются через боковую панель» | ✅ Верно | *«the skills, plugins, and connectors you use in Cowork work in the side panel too»* |
| «Качаем тут» (как будто всем) | ⚠️ Не всем | Боковая панель как сессия Cowork — пока **только Max и Team**, Pro «в ближайшие недели», Enterprise — если включит администратор |

## 🧩 Что с чем на самом деле синхронизируется

Пост склеил два разных продукта. Расширение — это **глаза и руки** Claude в браузере, а управлять им можно с трёх сторон, и роли у них разные:

| Откуда управляешь | Для чего это нужно |
| :--- | :--- |
| **Боковая панель** в самом Chrome | Работа на странице, ничего больше открывать не надо. Именно она стала сессией Claude Cowork |
| **Claude Cowork** (десктоп) | Когда браузер — лишь один шаг задачи, которая трогает ещё и локальные файлы. Десктоп должен быть запущен и подключён |
| **Claude Code** | Когда ты **разрабатываешь** тестируемый сайт: *«Build with Claude Code in your terminal, then deploy to a URL Claude can reach. Test and verify in the browser»* |

То есть «синхронизация сессий с Claude Code» из поста — это не про Claude Code. Синхронизируются сессии Cowork, и живут они **в аккаунте, а не на машине**. Claude Code получает другое: цикл сборки и проверки — верификация вёрстки по макету, чтение ошибок консоли и DOM, запланированные прогоны против регрессий.

> [!note] Важная оговорка из справки
> *«Tasks that need your local files, your computer, or Claude driving Chrome from another surface still need the **Claude Desktop app open and connected**, even though your session runs in the cloud.»*
>
> Облачная сессия не отменяет требования держать десктоп запущенным, если задача выходит за пределы вкладки.

## 🔐 Безопасность: prompt injection — главный риск, и цифры есть

Anthropic не прячет проблему, это стоит записать отдельно. Из описания в магазине:

> *«Websites can hide instructions that try to redirect Claude's actions.»*

Числа из их собственного тестирования:

| Конфигурация | Доля успешных атак |
| :--- | ---: |
| Без защит (пилот 2025) | **23,6 %** |
| Текущая конфигурация (внутренние тесты) | **менее 0,08 %** |

Прогресс огромный, но ноль — не ноль. Модель разрешений:

- **режим по умолчанию — «Automatically approve»**: Claude работает сам, а отдельная проверка безопасности просматривает каждое значимое действие и блокирует подозрительное;
- **«Manually approve»** — подтверждение каждого действия вручную, включается пользователем;
- по умолчанию **закрыты** сайты для взрослых и известные пиратские ресурсы, **финансовые сайты требуют отдельного разрешения**;
- на Team и Enterprise администратор включает расширение и задаёт список разрешённых сайтов организации.

> [!caution] Рекомендация самой Anthropic, а не моя
> *«We build defenses against this and test them, and we still recommend starting on sites you know, reading the prompts when they come, and telling us if Claude does something you didn't ask for.»*
>
> Практический вывод: не оставляй автоматический режим на страницах с чужим пользовательским контентом (форумы, комментарии, входящая почта, чужие issue на GitHub) — именно там прячут инъекции. И помни, что «Automatically approve» включён **сразу**, а не по твоему выбору.

## 🕵️ Что расширение собирает

Задекларировано в карточке магазина. Список исчерпывающий в прямом смысле:

- персональные данные (PII);
- **личная переписка**;
- местоположение;
- **история веба**;
- активность пользователя;
- **содержимое сайтов**.

Заявления разработчика: данные не продаются третьим лицам вне одобренных сценариев, не используются для целей вне основной функциональности, не применяются для оценки кредитоспособности.

Иначе и быть не может — агент, который читает страницу и кликает за тебя, физически обязан видеть всё, что видишь ты. Но это стоит осознавать: расширение с такими правами стоит держать выключенным на вкладках с банком, рабочей почтой и медицинскими данными, если ты не поставил там задачу осознанно.

> [!warning] Рейтинг 2,8 — но это, похоже, болезнь категории
> При 15 млн пользователей средняя оценка **2,8 из 5**. Для сравнения, в блоке «похожие» на той же странице расширение **ChatGPT** имеет 2,9, тогда как обычные утилиты рядом — 4,6–4,9. То есть низкая оценка типична для агентных браузерных расширений в целом, а не уникальная проблема Claude. Причины из отзывов я не разбирал — это отдельная работа.

## 💻 На твоих системах

Здесь для тебя главная практическая часть, и она безрадостная.

> [!danger] Только Google Chrome, никаких форков
> Из справки: *«Claude in Chrome is not supported on other Chromium-based web browsers or mobile devices»*. То есть **Brave, Edge, Vivaldi, Opera, обычный Chromium** — мимо. Нужен именно Google Chrome.

| Система | Что доступно |
| :--- | :--- |
| **Gentoo** (основная) | Расширение — да, если поставить `www-client/google-chrome` (не `chromium`). А вот **Claude Desktop на Gentoo официально не поддержан**: документация прямо говорит про Fedora и Arch *«run the CLI instead»*, и это же относится к Gentoo. Значит сценарий «начал в десктопе — продолжил в браузере» тебе недоступен; остаётся боковая панель + `claude` CLI |
| **Debian / Ubuntu** | Полный набор. Claude Desktop в бете с 30.06.2026: Ubuntu 22.04+ / Debian 12+, x86_64 или arm64, через apt-репозиторий Anthropic |
| **Arch** (планируется) | Расширение работает, десктопа нет — документация отправляет на CLI. Соберёшь `.deb` руками — не поддерживается |
| **Entware / RT-AX56U** | ❌ Неприменимо: ни браузера, ни графики |

Установка десктопа на Debian/Ubuntu — если решишь попробовать связку целиком:

```bash
sudo apt install curl gnupg
sudo curl -fsSLo /usr/share/keyrings/claude-desktop-archive-keyring.asc \
  https://downloads.claude.ai/claude-desktop/key.asc

# обязательно сверить отпечаток ключа
gpg --show-keys /usr/share/keyrings/claude-desktop-archive-keyring.asc
# ожидается: 31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE

echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/claude-desktop-archive-keyring.asc] \
https://downloads.claude.ai/claude-desktop/apt/stable stable main" \
  | sudo tee /etc/apt/sources.list.d/claude-desktop.list

sudo apt update && sudo apt install claude-desktop
```

> [!note] Сам себя приложение на Linux не обновляет
> *«The desktop app doesn't update itself on Linux»* — новые версии приезжают обычным `sudo apt update && sudo apt upgrade`.

### Cowork на Linux работает через виртуалку

Неочевидная деталь, которой нет ни в посте, ни в описании магазина: на Linux вкладка Cowork запускает задачи **в виртуальной машине под QEMU/KVM**. Требуется:

- аппаратная виртуализация, включённая в прошивке (иначе — «Cowork requires hardware virtualization (KVM)»);
- пакеты `qemu-system-x86`, `ovmf`, `virtiofsd` (ставятся как recommends; при `--no-install-recommends` их не будет);
- членство в группе `kvm`: `sudo usermod -aG kvm $USER`, затем перелогин — нужен доступ не только к `/dev/kvm`, но и к `/dev/vhost-vsock`;
- модуль ядра `vhost_vsock`: `sudo modprobe vhost_vsock`, для постоянства — `echo vhost_vsock | sudo tee /etc/modules-load.d/vhost_vsock.conf`.

Чего в Linux-бете нет вовсе: **Computer Use** (управление приложениями и экраном), диктовка голосом, а глобальный хоткей Quick Entry работает на X11, но на Wayland требует портала GlobalShortcuts от твоего окружения.

## 💡 Итог

Расширение — не новость и не про Claude Code. Что реально стоит знать:

- **сессии живут в аккаунте**, поэтому переход «панель → веб → десктоп → мобильный» действительно работает, и здесь пост прав;
- **это Cowork, а не Claude Code**; последний получает цикл «собрал → проверил в браузере», что тоже полезно, но это другое;
- боковая панель как Cowork-сессия пока **не у всех**: Max и Team, Pro в процессе выкатки;
- **режим по умолчанию — автоматический**, и при 15 млн установок и заявленных 0,08 % успешных инъекций это всё ещё поверхность атаки, которую стоит сужать вручную;
- на **Gentoo десктопной половины связки просто нет** — только Chrome с расширением и CLI.

## 🔗 Ссылки

- Пост: [t.me/bugnotfeature/27032](https://t.me/bugnotfeature/27032) (12.08.2026)
- Расширение: [Chrome Web Store](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn)
- Документация: [Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome) · [гайд по безопасности](https://support.claude.com/en/articles/12902428) · [Claude Desktop на Linux (beta)](https://code.claude.com/docs/en/desktop-linux)
- Связанные: [Claude Code — гайд](Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [Claude Code — шпаргалка команд](Claude%20Code%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4.md) · [MCP — серверы Model Context Protocol](Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md) · [Сводная таблица AI-агентов](%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82%202026%29.md) · [Tampermonkey — менеджер юзерскриптов](../../Apps/Browser-Extensions/Tampermonkey%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D1%8E%D0%B7%D0%B5%D1%80%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B2.md)

#AI #Claude #Anthropic #Браузер #Расширения #Безопасность #Приватность
