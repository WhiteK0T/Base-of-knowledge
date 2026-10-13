---
создал заметку: 2026-10-14T16:00:00
author: WhiteK0T
tags:
  - Programming
  - Квантовые_вычисления
  - Awesome
  - Python
  - Постквантовая_криптография
Источник:
  - https://t.me/open_source_friend/5863
  - https://github.com/qosf/awesome-quantum-software
  - https://qosf.org/
---

# ⚛️ awesome-quantum-software — каталог открытого квантового ПО

**[qosf/awesome-quantum-software](https://github.com/qosf/awesome-quantum-software)** — список открытых проектов для квантовых вычислений: библиотеки, симуляторы, компиляторы, коррекция ошибок, постквантовая криптография, игры. Ведёт **Quantum Open Source Foundation (QOSF)** с 2018 года, лицензия **CC0**, 2 411 звёзд. Новые проекты добавляются через pull request; последние добавления — 24.09.2026.

---

## 1. Что внутри

| Раздел | Проектов | Примеры |
| :--- | ---: | :--- |
| Полноценные библиотеки (full-stack) | 38 | Qiskit (IBM), Cirq (Google), PennyLane (Xanadu), CUDA-Q (NVIDIA), Braket (Amazon), Q# (Microsoft), pytket, Qibo |
| Симуляторы | 78 | Qiskit Aer, qsim, Stim, QuEST, Qrack, quimb, QuTiP, Yao.jl, Quirk (в браузере) |
| Отжиг (annealing) | 20 | инструменты D-Wave: dimod, Ocean, minorminer |
| Алгоритмы | 34 | |
| Компиляторы | 29 | TKET, PyZX, BQSKit, Mitiq (снижение ошибок), Catalyst, MQT QMAP |
| Коррекция ошибок | 10 | PyMatching, Stim-совместимые декодеры, MQT QECC |
| Квантовая и постквантовая криптография | 9 | liboqs, PQClean, форки OpenSSL и OpenSSH |
| Экспериментальное оборудование | 18 | |
| Инструменты | 31 | |
| Игры и развлечения | 15 | Quandoom (DOOM для квантового компьютера), Entanglion (настольная игра) |
| Прочее (аналоговые гамильтонианы, конвертеры, ассемблеры, управление, совместимость, данные) | 19 | |
| **Заброшенные** (отдельный раздел) | 27 | |
| **Итого** | **328** | |

Внутри разделов проекты сгруппированы по языкам: Python, C++, Julia, Rust, JavaScript, Q#, Common Lisp и другие.

---

## 2. Насколько список свежий

Пост называет список регулярно обновляемым — **новые проекты добавляются, но старые почти не вычищаются**. Проверка последних коммитов 262 GitHub-проектов из рабочих разделов (14.10.2026):

| Последний коммит | Проектов |
| :--- | ---: |
| меньше года назад | **132** (50%) |
| 1–2 года назад | 23 |
| **больше 2 лет назад** | **101** (39%) |
| репозиторий удалён (404) | 6 |

У раздела «Заброшенные» критерий — **2 года без активности**, но 101 проект с таким сроком всё ещё стоит в рабочих разделах. Встречаются и устаревшие названия: например, **Qiskit Terra** давно влит в основной пакет `qiskit`, а Qiskit почему-то значится и в разделе **C**. Перед использованием проекта загляните в его репозиторий.

---

## 3. С чего начать

| Задача | Что взять |
| :--- | :--- |
| Изучить квантовые схемы без установки | **[Quirk](https://algassert.com/quirk)** — схемы перетаскиванием прямо в браузере |
| Основной инструмент для программирования | **Qiskit** + симулятор **Qiskit Aer** — самая большая экосистема и учебные материалы |
| Альтернатива от Google | **Cirq** + **qsim** |
| Квантовое машинное обучение | **PennyLane** (дифференцируемые схемы, интеграция с PyTorch и JAX) |
| Симуляция на GPU | **CUDA-Q**, qsim, PennyLane Lightning |
| Коррекция ошибок | **Stim** (быстрый симулятор стабилизаторных схем) + **PyMatching** (декодер) |
| Оптимизация схем | **PyZX** (ZX-исчисление), **TKET** |
| Задачи оптимизации (QUBO) | **dimod** и инструменты D-Wave |

### Qiskit на своей машине

Ставится через `pip` в виртуальное окружение — одинаково на всех дистрибутивах:

| Система | Подготовка |
| :--- | :--- |
| **Gentoo** | `emerge --ask dev-lang/python` (обычно уже есть) |
| **Debian / Ubuntu** | `sudo apt install python3-venv python3-pip` |
| **Arch** | `sudo pacman -S python python-pip` |
| **Entware** | не подходит: колёса Qiskit и Aer собраны под x86_64 и aarch64 с glibc, а симуляция требует памяти. Для знакомства — Quirk в браузере |

```bash
python3 -m venv ~/qenv && . ~/qenv/bin/activate
pip install qiskit qiskit-aer
```

Первая программа — состояние Белла (два запутанных кубита):

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2)
qc.h(0)          # суперпозиция на первом кубите
qc.cx(0, 1)      # запутываем со вторым
qc.measure_all()

sim = AerSimulator()
counts = sim.run(transpile(qc, sim), shots=1000).result().get_counts()
print(counts)    # примерно {'00': 500, '11': 500}
```

Полный вектор состояний на симуляторе растёт как 2ⁿ: 30 кубитов — это уже около 16 ГБ памяти, поэтому большие схемы считают на GPU или специальными методами (тензорные сети, стабилизаторы).

> [!note] Облачные квантовые компьютеры
> Запуск на настоящем железе — через облака IBM Quantum, Amazon Braket и других — требует аккаунта у провайдера. Из России доступ к ним может быть ограничен. Локальные симуляторы работают без ограничений.

---

## 4. Постквантовая криптография на практике

В разделе криптографии стоят форки **OpenSSL и OpenSSH с постквантовыми алгоритмами** от Open Quantum Safe. Сейчас они для практики почти не нужны:
- **OpenSSL 3.5+** сам поддерживает ML-KEM, ML-DSA и SLH-DSA (форк OQS не обновлялся с января 2025);
- **OpenSSH 10.0+** по умолчанию использует гибридный обмен ключами `mlkem768x25519-sha256`.

Для экспериментов и других алгоритмов остаются **liboqs** и **PQClean**. Связанные заметки в базе: [Ключи в Java (JCA) — включая постквантовые](../Java/Crypto/%D0%9A%D0%BB%D1%8E%D1%87%D0%B8%20%D0%B2%20Java%20%28JCA%29%20%E2%80%94%20%D1%87%D1%82%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyFactory%20%D0%B8%20%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyPairGenerator%20%28SPI%2C%20KeySpec%2C%20PEM-DER%2C%20ECC%2C%20%D0%BF%D0%BE%D1%81%D1%82%D0%BA%D0%B2%D0%B0%D0%BD%D1%82%29.md), [SSH-ключи](../../Network/SSH/SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md).

## 🔗 Ссылки

- Список: https://github.com/qosf/awesome-quantum-software
- Quantum Open Source Foundation: https://qosf.org/
- Qiskit: https://www.ibm.com/quantum/qiskit · документация: https://quantum.cloud.ibm.com/docs
- Quirk: https://algassert.com/quirk
- Open Quantum Safe (liboqs): https://openquantumsafe.org/
- Исходный пост: https://t.me/open_source_friend/5863

#Programming #Квантовые_вычисления #Awesome #Python #Постквантовая_криптография
