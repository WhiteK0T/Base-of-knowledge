---
создал заметку: 2026-09-10T11:00:00
author: WhiteK0T
tags:
  - Безопасность
  - Windows
  - Zero-day
  - Defender
  - LPE
  - Раскрытие_уязвимостей
Источник:
  - https://t.me/IzHmfluzM81OTAy/616
  - https://deadeclipse666.blogspot.com/2026/06/its-patch-tuesday.html
  - https://www.picussecurity.com/resource/blog/rogueplanet-anatomy-of-the-nightmare-eclipse-microsoft-defender-zero-day
  - https://git.projectnightcrawler.dev/NightmareEclipse/LegacyHive
---

# 🌑 Nightmare Eclipse против Microsoft — RoguePlanet, GreatXML и LegacyHive

Исследователь под ником **Nightmare Eclipse (NE)** с апреля 2026 ведёт открыто конфронтационную кампанию против практик раскрытия и bug bounty у Microsoft: публичные zero-day без координации, в ответ — блокировка аккаунта для подачи уязвимостей и снос репозиториев на GitHub и GitLab. К моменту выхода RoguePlanet это была уже **седьмая публичная PoC zero-day с начала апреля 2026** (оценка Picus Security).

Заметка разбирает виток июнь–июль 2026 и **добавляет то, чего в исходном дайджесте быть не могло**: что Microsoft закрыла за август.

> [!warning] Это не «истории из твиттера» — инструменты уходят в бой
> Huntress сообщала, что более ранний инструментарий NE — **BlueHammer, RedSun и UnDefend** — использовался в **реальной цепочке атаки**. То есть публикации этого исследователя не оседают в коллекциях, а операционализируются злоумышленниками. **BlueHammer** получил **CVE-2026-33825** (CVSS 7.8, «Insufficient granularity of access control in Microsoft Defender», опубликована 14.04.2026) и на момент разбора Picus числился **активно эксплуатируемым**.

---

## 📅 Что произошло

### 9 июня — отмена «массового слива» и извинения

NE опубликовал PGP-подписанное заявление: обещанного на 14 июля массового раскрытия не будет.

> (Un)fortunately I will be unable to mass disclose zerodays in July 14th, RoguePlanet took way more time than expected and truly drained me… **I did not intend to spread a mass panic with that post and I apologize for doing so.**

В том же посте про RoguePlanet он описывает цену вопроса прямым текстом: три недели без нормального сна и еды, «3 часа сна после 96 часов непрерывной работы», серьёзно просевшее физическое и психическое состояние. Это не деталь для колорита — именно из-за этого и сорвалась объявленная дата.

### 9 июня — RoguePlanet: гонка в Defender до SYSTEM

Опубликован в тот же день, **в течение нескольких часов после июньского Patch Tuesday** — третий месяц подряд, когда NE подгадывает zero-day под день патчей.

**Механика.** TOCTOU-гонка в пути обработки файлов Microsoft Defender. Движок работает как `MsMpEng.exe` под службой `WinDefend` от SYSTEM — это by design, чтобы иметь право удалить или переписать вредоносный файл где угодно на диске. Обратная сторона: **любая файловая операция Defender выполняется с правами SYSTEM**, и если успеть подменить цель между проверкой и использованием, привилегированная запись уходит туда, куда нужно атакующему. Успешный запуск даёт `cmd.exe` от `NT AUTHORITY\SYSTEM`.

**Важные оговорки из разбора Picus:**

| | |
| :--- | :--- |
| **Работает на полностью пропатченных** | Windows 10 и 11, включая июньский Patch Tuesday 2026 (проверено на Windows 11 с KB5094126) |
| **CVE на момент публикации** | нет ни CVE, ни advisory, ни целевого патча |
| **Надёжность** | это гонка, то есть вероятностная: «почти 100 % на одном железе, почти бесполезно на другом». Ненадёжность — операционная деталь, а **не** мера защиты |
| **Что блокирует** | **allowlisting приложений**: ThreatLocker независимо воспроизвели эксплойт и сообщили, что их дефолтный allowlisting не дал ему выполниться |
| **Как ловить** | интерактивная оболочка с целостностью SYSTEM, у которой **родитель — `MsMpEng.exe`**. В здоровой системе такой цепочки не бывает |

Отдельная деталь, которую NE добавил через несколько дней: **BlueHammer, RedSun и RoguePlanet используют внутренний флаг `MPSCAN_OPTION_NOCONSOLIDATE`**, из-за чего при успешной эксплуатации Defender **не показывает пользователю всплывающее уведомление** об обнаружении угрозы. То есть атака ещё и тихая.

Июньский Patch Tuesday, к слову, закрыл две другие его находки — **GreenPlasma и YellowKey**, — но этот путь оставил открытым.

### 10 июня — GreatXML: обход BitLocker через Defender Offline Scan

Развитие идей YellowKey. Связка **Microsoft Defender Offline Scan + WinRE**: доверенная среда восстановления Windows по-прежнему годится для обхода защиты BitLocker.

Из первоисточника, дословно:

> This was an **accidental discovery, it took a total of 4 hours** to find this. **If you ever attempted to use Windows Defender Offline Scan, you're automatically vulnerable** to a bitlocker bypass.

Опубликован сразу в трёх местах — `git.projectnightcrawler.dev`, `github.com/MSNightmare`, `git.churchofmalware.org`. Логика NE после сноса аккаунтов: *«Microsoft forgot that even if they banned my GitLab and Github accounts, they cannot unwrite my code. Once it's public, you can't remove it»*.

### 3 июля — «самое неинтересное, что я публиковал»

Обещанную более серьёзную находку NE решил не публиковать — нужна доработка. Взамен анонсировал ещё одну июльскую публикацию, заранее её обесценив:

> it will be the **least interesting and least impactful bug** I dropped since I started

### 14 июля — LegacyHive: чужие ветки реестра в ProfSvc

Zero-day в **Windows User Profile Service (ProfSvc)**: ошибка при загрузке файлов реестра позволяет локальному пользователю работать с чужими registry hive.

Из README репозитория:

> The PoC **requires another standard user credentials and a third username** (which can be an administrator account); if successful, it will end up mounting the target user hive in current user classes root.
>
> The PoC was **stripped down as an attempt to prevent public exploitation** — the original PoC did not require additional user credential and was not limited to `usrclass.dat` hive, any hive could be loaded.
>
> The PoC is fully functional in all currently supported desktop and server installation **with July 2026 patch**.

То есть опубликованная версия намеренно урезана и служит скорее заготовкой для дальнейшего исследования, чем готовым инструментом получения SYSTEM. Репозиторий на самохостинге NE: 4 коммита, один файл `LegacyHive.cpp`, залит 14.07.2026.

---

## ✅ Что закрыто к сентябрю 2026 (чего не было в дайджесте)

Дайджест писался в июле, когда LegacyHive был непропатчен, а у RoguePlanet не было CVE. Прошёл через бюллетени MSRC за июль–сентябрь и нашёл совпадения по компоненту и классу. Microsoft в благодарностях указывает **«Anonymous»** и эксплойты по именам не называет, поэтому это сопоставление, а не официальное подтверждение — но совпадает всё:

| Patch Tuesday | CVE | Заголовок MSRC | Благодарность | Похоже на |
| :--- | :--- | :--- | :--- | :--- |
| **июль 2026** | **CVE-2026-50661** | Windows BitLocker Security Feature Bypass Vulnerability | Anonymous | **GreatXML** |
| **август 2026** | **CVE-2026-62832** | Windows User Profile Service Elevation of Privilege Vulnerability (CWE-59, CVSS 7.8) | Anonymous | **LegacyHive** |
| **август 2026** | **CVE-2026-69414** | Microsoft Defender Elevation of Privilege Vulnerability | Anonymous | **RoguePlanet** |

Плюс в июле прошли два **Microsoft Defender Remote Code Execution** (CVE-2026-55011 и CVE-2026-55012), тоже с благодарностью «Anonymous».

**Практический вывод:** если система обновлялась штатно, к сентябрю 2026 весь разобранный здесь набор, судя по всему, закрыт. Актуальный риск — у машин, застрявших на июньских или июльских обновлениях.

---

## 🧭 Как менялся подход, а не находки

Главное изменение за этот виток — не в технике, а в стратегии публикации. Вместо анонсированного массового раскрытия NE перешёл к **последовательному выпуску отдельных PoC**, часть наработок оставляя непубличной, а часть публикуемых — намеренно урезанной. MSRC со своей стороны выпустила пост о координированном раскрытии, где упоминается работа с правоохранителями против «malicious activity» — что широко прочитали как адресованное этому исследователю.

> [!note] Пара ссылок из дайджеста уже мертва
> Проверил все источники поста: материал The Register про LegacyHive по указанному адресу отдаёт **404**, и запись в блоге `projectnightcrawler.dev` от 15.06.2026 — тоже **404**. Живы: блог `deadeclipse666.blogspot.com`, самохостовый Gitea NE и разборы Picus/Cyderes. Для истории, которая держится на «once it's public, you can't remove it», это довольно иронично — и хороший аргумент держать локальные копии.

---

## 🛡️ Что делать пользователю Windows

Владельцу это касается только Windows-машины (основная система — Gentoo), но набор мер универсальный:

1. **Обновляться штатно.** По совпадениям выше весь разобранный набор закрыт к августовскому Patch Tuesday. Проверить: `winver` и `Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5`.
2. **Проверить версию платформы и движка Defender отдельно** — она обновляется не вместе с накопительным пакетом:
   ```powershell
   Get-MpComputerStatus | Select-Object AMProductVersion, AMEngineVersion, AntivirusSignatureVersion
   Update-MpSignature
   ```
3. **Allowlisting приложений** — единственная мера, про которую в разборе RoguePlanet прямо сказано, что она сработала. На домашней машине это AppLocker или WDAC.
4. **Ловить аномальную родословную процессов.** Интерактивная оболочка от SYSTEM с родителем `MsMpEng.exe` — сигнал, которого в норме не существует. Смотреть удобно через [System Informer](../../../Windows/System%20Informer%20%E2%80%94%20%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%B2%20%D0%B8%20%D0%BE%D1%85%D0%BE%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%BC%D0%B0%D0%BB%D0%B2%D0%B0%D1%80%D1%8C%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20Process%20Hacker%29.md).
5. **Про BitLocker:** если когда-либо запускался Microsoft Defender Offline Scan — по словам автора GreatXML, машина автоматически попадала в зону риска. Отдельная причина не откладывать июльские обновления.

| Система | Актуальность |
| :--- | :--- |
| **Windows** | ✅ напрямую: LPE до SYSTEM, обход BitLocker, тихая работа мимо уведомлений Defender |
| **Gentoo / Debian-Ubuntu / Arch** | ➖ не затронуты — всё завязано на Defender, WinRE и ProfSvc. Полезно как модель угрозы: «привилегированный антивирус как примитив записи» |
| **Entware / RT-AX56U** | ➖ нерелевантно |

---

## 🔗 Связанные заметки

- Другая техника эскалации в Windows, тоже без LSASS: [Impersonate (SensePost)](../../Impersonate%20%28SensePost%29%20%E2%80%94%20%D0%BE%D0%BB%D0%B8%D1%86%D0%B5%D1%82%D0%B2%D0%BE%D1%80%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20Windows%20%D0%B4%D0%BB%D1%8F%20%D1%8D%D1%81%D0%BA%D0%B0%D0%BB%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B4%D0%BE%20domain%20admin%20%D0%B1%D0%B5%D0%B7%20LSASS%20%28%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20%D1%84%D0%B0%D0%BA%D1%82%D1%8B%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D1%85%D0%B0%D0%B9%D0%BF%D0%B0%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md)
- Чем смотреть родословную процессов и ловить аномалии: [System Informer](../../../Windows/System%20Informer%20%E2%80%94%20%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%B2%20%D0%B8%20%D0%BE%D1%85%D0%BE%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%BC%D0%B0%D0%BB%D0%B2%D0%B0%D1%80%D1%8C%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20Process%20Hacker%29.md)
- Контроль исходящих соединений на Windows: [Fort Firewall](../../../Windows/Fort%20Firewall%20%28tnodir%29%20%E2%80%94%20%D0%BE%D0%BF%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%81%D0%BD%D1%8B%D0%B9%20%D0%B1%D1%80%D0%B0%D0%BD%D0%B4%D0%BC%D0%B0%D1%83%D1%8D%D1%80%20Windows%20%D0%BD%D0%B0%20%D1%81%D0%B2%D0%BE%D1%91%D0%BC%20WFP-%D0%B4%D1%80%D0%B0%D0%B9%D0%B2%D0%B5%D1%80%D0%B5%20%28per-app%2C%20%D0%BB%D0%B8%D0%BC%D0%B8%D1%82%D1%8B%2C%20%D0%BD%D0%BE%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%20HVCI%29.md)
- Ещё одна июльская история про доверенный компонент, который сработал против владельца: [AsyncAPI](../Apps/AsyncAPI%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20%D1%81%D0%BE%D0%B1%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20CI-CD%20%285%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20npm%20%D1%81%20%D0%B2%D0%B0%D0%BB%D0%B8%D0%B4%D0%BD%D1%8B%D0%BC%20provenance%2C%20Miasma%20v3%2C%20%D1%81%D1%80%D0%B0%D0%B1%D0%B0%D1%82%D1%8B%D0%B2%D0%B0%D0%B5%D1%82%20%D0%BF%D1%80%D0%B8%20require%29.md)

## 🔗 Ссылки

- Блог NE (PGP-подписанные посты): [deadeclipse666.blogspot.com](https://deadeclipse666.blogspot.com/) · [blog.projectnightcrawler.dev](https://blog.projectnightcrawler.dev/posts/2026-07-03-july-updates/)
- Репозитории: [LegacyHive](https://git.projectnightcrawler.dev/NightmareEclipse/LegacyHive) · [GreatXML](https://git.projectnightcrawler.dev/NightmareEclipse/GreatXML)
- Разборы: [Picus — RoguePlanet](https://www.picussecurity.com/resource/blog/rogueplanet-anatomy-of-the-nightmare-eclipse-microsoft-defender-zero-day) · [Cyderes — GreatXML](https://www.cyderes.com/howler-cell/greatxml-windows-zero-day)
- CVE: [CVE-2026-33825 (BlueHammer)](https://nvd.nist.gov/vuln/detail/CVE-2026-33825) · [CVE-2026-62832](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-62832) · [CVE-2026-69414](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-69414) · [CVE-2026-50661](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-50661)
- Источник новости: [@Mr0x45xploit](https://t.me/IzHmfluzM81OTAy/616)

#Безопасность #Windows #Zero-day #Defender #LPE #Раскрытие_уязвимостей
