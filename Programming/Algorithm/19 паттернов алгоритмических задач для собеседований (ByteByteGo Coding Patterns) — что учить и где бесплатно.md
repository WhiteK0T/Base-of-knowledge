---
создал заметку: 2026-07-25T14:30:00
author: WhiteK0T
tags:
  - Алгоритмы
  - Собеседования
  - Паттерны
  - LeetCode
  - Подготовка
  - Карьера
Источник:
  - https://t.me/proglibrary/11746
  - https://bytebytego.com/exercises/coding-patterns
---

# 🧩 19 паттернов алгоритмических задач для собеседований

**Идея (и она правильная):** большинство задач на технических собеседованиях сводится к **ограниченному набору шаблонов решения**. Выучив ~**19 паттернов**, ты решаешь и **незнакомые** задачи — вместо зубрёжки сотен отдельных решений с LeetCode. Пост из [@proglibrary](https://t.me/proglibrary/11746) рекламирует подборку **101 задачи по 19 паттернам**.

> [!warning] Честно про источник: это платный ByteByteGo, а не бесплатная «подборка»
> Пост предлагает «сохранить подборку», но ссылка (через сокращатель `clc.to` с UTM-метками) ведёт на **[ByteByteGo → Coding Patterns](https://bytebytego.com/exercises/coding-patterns)** — платформу **Alex Xu** (автора книг «System Design Interview»). Это **платная подписка** (порядка ~$499/год или lifetime, часто со скидками); часть контента бесплатна, но 101 задача с решениями — в основном **за пейволом**. То есть «сохраняйте подборку» — это маркетинг к платному продукту, а не ссылка на бесплатный список.
>
> **Что реально ценно и бесплатно** — сама **таксономия из 19 паттернов** (ниже). Она де-факто отраслевой стандарт и почти совпадает у Grokking / NeetCode / AlgoMonster. Учить паттерны можно **бесплатно** (см. раздел с альтернативами) — платить за ByteByteGo не обязательно.

> [!tip] Почему «паттерны, а не зубрёжка» — это правда работает
> Подход одобрен практически всеми (NeetCode, Grokking the Coding Interview и т.д.): ты учишь **приём** (скользящее окно, два указателя, DP…) и **распознавание**, к какому паттерну свести задачу. Это масштабируется на новые задачи, а зубрёжка N решений — нет. Так что **метод бери, а платформу выбирай по кошельку**.

## 📋 Те самые 19 паттернов (что это и когда применять)

| # | Паттерн | Когда применять | Типовые задачи |
| :---: | :--- | :--- | :--- |
| 1 | **Two Pointers** | пара/тройка в **отсортированном** массиве, сходящиеся/расходящиеся указатели | Two Sum II, 3Sum, Container With Most Water |
| 2 | **Hash Maps & Sets** | O(1) поиск/подсчёт/дедуп | Two Sum, Group Anagrams, Longest Consecutive Sequence |
| 3 | **Linked Lists** | in-place разворот, манипуляции указателями | Reverse Linked List, Merge Two Sorted Lists |
| 4 | **Fast & Slow Pointers** | цикл, середина списка, «черепаха и заяц» (Флойд) | Linked List Cycle, Happy Number, Middle of List |
| 5 | **Sliding Window** | **непрерывный** подотрезок/подстрока с условием | Longest Substring Without Repeating, Min Window Substring |
| 6 | **Binary Search** | поиск в отсортированном **или по «пространству ответов»** | Search in Rotated Sorted Array, Koko Eating Bananas |
| 7 | **Stacks** | LIFO, парность, **монотонный стек** | Valid Parentheses, Daily Temperatures |
| 8 | **Heaps (Priority Queue)** | top-K, медиана потока, k-way merge | Kth Largest, Merge K Sorted Lists, Median from Data Stream |
| 9 | **Intervals** | слияние/пересечение отрезков | Merge Intervals, Insert Interval, Meeting Rooms |
| 10 | **Prefix Sums** | быстрые суммы на диапазонах | Subarray Sum Equals K, Range Sum Query |
| 11 | **Trees** | обходы DFS/BFS, свойства дерева | Level Order Traversal, Validate BST, Max Depth |
| 12 | **Tries** | префиксные деревья, автодополнение | Implement Trie, Word Search II |
| 13 | **Graphs** | BFS/DFS, топосорт, **union-find** | Number of Islands, Course Schedule, Clone Graph |
| 14 | **Backtracking** | перебор комбинаций/перестановок/подмножеств | Subsets, Permutations, N-Queens, Word Search |
| 15 | **Dynamic Programming** | перекрывающиеся подзадачи, оптимум | Climbing Stairs, House Robber, Coin Change, LCS |
| 16 | **Greedy** | локально-оптимальный выбор ведёт к глобальному | Jump Game, Gas Station |
| 17 | **Sort & Search** | предобработка сортировкой, свои компараторы | сортировочные варианты, Merge Intervals-подобные |
| 18 | **Bit Manipulation** | XOR-трюки, битовые маски | Single Number, Counting Bits |
| 19 | **Math & Geometry** | теория чисел, геометрия, работа с матрицей | Rotate Image, Pow(x, n), Happy Number |

## 🆓 Где учить те же паттерны бесплатно

| Ресурс | Что даёт |
| :--- | :--- |
| **NeetCode** ([neetcode.io](https://neetcode.io)) | Лучшая бесплатная точка входа: **NeetCode 150 / roadmap**, разбитый по этим же паттернам, бесплатные видеоразборы |
| **Sean Prashad — Leetcode Patterns** ([seanprashad.com/leetcode-patterns](https://seanprashad.com/leetcode-patterns/)) | Курируемый список задач с тегами паттернов и фильтрами |
| **«14 Patterns to Ace Any Coding Interview»** | Классическая бесплатная статья (Design Gurus / hackernoon) — основа «паттерного» подхода |
| **LeetCode** (Explore-карточки, бесплатный тариф) | Сами задачи + теги; тренируешь на практике |
| **TheAlgorithms** (репозиторий) | Референсные реализации алгоритмов на разных языках — см. [TheAlgorithms](TheAlgorithms%20%E2%80%94%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5%20%D1%80%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D0%BE%D0%B2%20%D0%B8%20%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85%20%D0%BD%D0%B0%20%D0%B4%D0%B5%D1%81%D1%8F%D1%82%D0%BA%D0%B0%D1%85%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%BE%D0%B2%20%28%D1%87%D1%82%D0%BE%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8%2C%20%D0%B4%D0%BB%D1%8F%20%D1%87%D0%B5%D0%B3%D0%BE%2C%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B%29.md) |

> [!note] Платные (для полноты картины)
> **ByteByteGo** (эта подборка), **Grokking the Coding Interview** (Design Gurus / educative — «прародитель» паттерн-подхода), **AlgoMonster** — все учат по сути одному и тому же набору. Платить стоит только если нужны структурированные разборы «под ключ» и не жалко денег; для самоподготовки бесплатных ресурсов выше достаточно.

## 🎯 Как учить (практический план)

1. Пройди список паттернов выше, для каждого — **1–2 эталонные задачи**, пока не «щёлкнет» приём.
2. Дальше решай задачи, **сначала называя паттерн**, а уже потом код (главный навык — распознавание).
3. Возвращайся к тяжёлым (DP, Graphs, Backtracking) чаще — там больше всего вариаций.
4. Порядок для новичка: Two Pointers → Hash → Sliding Window → Binary Search → Stacks/Heaps → Trees → Graphs → Backtracking → DP.

## 🖥️ Применимость

Это **учебный** материал — от ОС не зависит, нужен лишь браузер и любой язык (владельцу подойдёт то, на чём он пишет). Актуально для подготовки к **техсобеседованиям** и общего роста в алгоритмах; как система знаний хорошо ложится рядом с самообучением CS.

## 🔗 Связанные заметки

- Референсные реализации алгоритмов (TheAlgorithms и пр.): [TheAlgorithms](TheAlgorithms%20%E2%80%94%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5%20%D1%80%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D0%BE%D0%B2%20%D0%B8%20%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85%20%D0%BD%D0%B0%20%D0%B4%D0%B5%D1%81%D1%8F%D1%82%D0%BA%D0%B0%D1%85%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%BE%D0%B2%20%28%D1%87%D1%82%D0%BE%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8%2C%20%D0%B4%D0%BB%D1%8F%20%D1%87%D0%B5%D0%B3%D0%BE%2C%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B%29.md)
- Системный путь в Computer Science по курсам топ-вузов: [CS Self-learning (CSDIY)](../../Education/CS%20Self-learning%20%28CSDIY%2C%20csdiy.wiki%29%20%E2%80%94%20%D0%B3%D0%B8%D0%B4%20%D0%BF%D0%BE%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%BC%D1%83%20%D0%B8%D0%B7%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8E%20Computer%20Science%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D0%B0%D0%BC%20%D1%82%D0%BE%D0%BF-%D0%B2%D1%83%D0%B7%D0%BE%D0%B2.md)
- Бесплатные курсы с сертификатами (в т.ч. алгоритмы/CS): [awesome-certificates](../../Education/awesome-certificates%20%28PanXProject%29%20%E2%80%94%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20200%2B%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D1%85%20%D0%BA%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D1%81%20%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%D0%BC%D0%B8%20%28IT-CS-%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81%29%2C%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B.md)

## 🔗 Ссылки

- Первоисточник подборки (платно): [ByteByteGo — Coding Patterns](https://bytebytego.com/exercises/coding-patterns)
- Бесплатно по тем же паттернам: [NeetCode](https://neetcode.io) · [Leetcode Patterns (Sean Prashad)](https://seanprashad.com/leetcode-patterns/)
- Источник новости: [@proglibrary](https://t.me/proglibrary/11746)

#Алгоритмы #Собеседования #Паттерны #LeetCode #Подготовка #Карьера
