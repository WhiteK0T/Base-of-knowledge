---
создал заметку: 2026-09-09T18:40:00
author: WhiteK0T
tags:
  - DevOps
  - Kubernetes
  - Terraform
  - AWS
  - CI-CD
  - DevSecOps
  - Подборка
  - Карьера
Источник:
  - https://t.me/bugnotfeature/27570
  - https://github.com/DevCloudNinjas/DevOps-Projects
  - https://devcloudninjas.github.io/DevOps-Projects/
---

# 🛠️ DevOps-Projects (DevCloudNinjas) — 54 проекта «для резюме»: что там правда, а что нет

**DevOps-Projects** ([github.com/DevCloudNinjas/DevOps-Projects](https://github.com/DevCloudNinjas/DevOps-Projects)) — сборник практических DevOps-лабораторных: Terraform, Kubernetes, Docker, CI/CD, DevSecOps, AWS, Azure. **617★, 463 форка, MIT**, живёт с 17.02.2024. Есть живой сайт-портал на Astro Starlight: [devcloudninjas.github.io/DevOps-Projects](https://devcloudninjas.github.io/DevOps-Projects/).

> [!info] Коротко
> Проектов действительно **54** — это правда. Но «забрать любой проект» не выйдет: **10 из 54 состоят из двух файлов** (README + метаданные), а **все 6 ссылок на «подробный гайд в блоге» отдают 404**. Почти всё завязано на **AWS (36 проектов против 5 на Azure)**, и репозиторий **сам помечает 13 проектов как `cost_risk: high`** — один только контрол-плейн EKS стоит **$0,10/час ≈ $73/мес**. А ещё в репозитории лежит готовый **маркетинг-кит с постами в LinkedIn от первого лица** («I built and modernized a multi-project DevOps lab») и прайс от **$29 до $7 500**.

---

## ✅ Проверка заявлений из поста

| Заявление | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «54 проекта разной сложности» | ⚠️ | Каталогов `project-01`…`project-54` ровно **54** ✅. Но **сложность нигде не размечена**: в `project.yaml` поля difficulty нет, а обещанный в `PROJECTS.md` опциональный блок `learning:` (`estimated_time`, `prerequisites`) **отсутствует у всех 54** |
| «по Terraform, Kubernetes, Docker, CI/CD, DevSecOps, AWS, Azure **и другим подтемам**» | ⚠️ | По их же метаданным: Docker 21, Kubernetes 21, Terraform 19/22, но **cloud: aws 36 против azure 5**, GCP — **ноль**. «Другие подтемы» — это в основном ещё раз AWS |
| «гора лабораторных с пошаговыми гайдами **и конфигами**» | ⚠️ | Гайды есть, местами очень подробные (README до **40 КБ**), плюс папка `learning/` на **3567 файлов**. Но конфиги не везде: **10 проектов = README + `project.yaml`**, и сам репозиторий помечает **11 как `reference_only`** |
| «Можно забрать **любой** проект» | ❌ | «Любой» — нет. 10 проектов помечены `status: reference`; у 6 весь смысл в ссылке на блог автора, **и все 6 статей удалены (HTTP 404)**; в части лабораторных мёртвые репозитории приложений, которые надо собирать |
| «разобраться, **переписать под себя**» | ✅ | Верно — только это **не опция, а обязательный шаг**: `cluster_version = "1.27"/"1.29"` уже вне календаря поддержки EKS, `trivy_0.43.0.deb` качается 404-й, `actions/checkout@v2` и образы `microsoft/dotnet:2.1-nanoserver` |
| «закинуть в своё портфолио» | ⚠️ | Юридически можно (MIT/Apache/AGPL). Но форков **463**, README у всех одинаковые, а сам репозиторий раздаёт **готовые посты в LinkedIn от первого лица** — это отдельный разговор, см. ниже |
| Про деньги | ❌ | В посте **ни слова**. Репозиторий честнее поста: 13 проектов помечены `cost_risk: high`, есть отдельный ранбук по стоимости — а на сайте прайс от **$29 до $7 500** |

---

## 📦 Что это на самом деле

Это **не авторский курс, а агрегатор**. Ключевой коммит от 20.02.2026 называется прямо:

> `Complete repo overhaul: consolidate 58 org repos into unified structure`

То есть 58 разрозненных репозиториев организации свалили в один. Отсюда особенности:

- **Всего 56 коммитов** на 6338 файлов — материал заезжал огромными пачками.
- **Клон весит 757 МБ.** Основной объём — папка `learning/` (3567 файлов) с **вендорными копиями чужих курсов**: `containers-fundamentals` (MIT © 2021 Kubernetes Academy Online), `devops-201-track` (MIT © 2023 Lionel Tchami), `kubernetes-cka-prep` (MIT © 2022 Ali), `devops-bootcamp`. Лицензии позволяют, но авторство — не автора репозитория.
- **15 проектов иллюстрированы картинками с `miro.medium.com`** — 596 из 1068 ссылок в README ведут на CDN Medium. Это следы статей, перенесённых в репозиторий. Сами картинки живы (выборка из 30 — все 200).

> [!warning] master стоит с 14 июня 2026
> GitHub показывает «обновлено 27.08.2026» — но это ветка `solution-paths-recovery` (10 коммитов, `INSTRUCTOR_SOLUTION_PACK.md` и «live pilot execution pack»). **В `master` последний коммит — 14.06.2026**, и клонируется именно он.
> А `homepage` в метаданных репозитория ведёт на зеркало [gitlab.com/devcloudninjas1/devops-projects](https://gitlab.com/devcloudninjas1/devops-projects) — там **последняя активность 12.10.2024 и 0 звёзд**.

---

## 📊 Цифры из их собственных метаданных

У каждого из 54 проектов есть `project.yaml` по схеме `project.schema.json`. Это редкая и полезная вещь — репозиторий сам себя классифицирует. Свёл всё в таблицы:

| `classification` | шт. |
| :--- | ---: |
| deployable | 36 |
| learning | 18 |

| `status` | шт. | | `deployability` | шт. |
| :--- | ---: | :--- | :--- | ---: |
| cloud_lab | 23 | | ci_cd_ready | 23 |
| **reference** | **10** | | **reference_only** | **11** |
| devsecops_lab | 10 | | iac_ready | 10 |
| local_lab | 4 | | container_ready | 4 |
| local_validated | 3 | | kubernetes_ready | 4 |
| ci_lab | 2 | | local_only | 2 |
| local_demo | 2 | | | |

| `cost_risk` | шт. | | Облако | шт. | | CI/CD | шт. |
| :--- | ---: | :--- | :--- | ---: | :--- | :--- | ---: |
| medium | 32 | | aws | 36 | | jenkins | 12 |
| **high** | **13** | | azure | 5 | | azure-devops | 5 |
| low | 9 | | gcp | 0 | | github-actions | 5 |
| | | | | | | argocd | 5 |
| | | | | | | aws-codepipeline | 3 |
| | | | | | | gitlab-ci | 1 |

IaC: `terraform` — 22 проекта (217 файлов `.tf`), `sam` — 1. Манифесты Kubernetes есть в 18 проектах, `Dockerfile`/`Jenkinsfile`/`Makefile` — 63 штуки.

---

## 🕳️ Десять проектов, которых почти нет

10 проектов состоят ровно из двух файлов — `README.md` и `project.yaml`. Причём это две разные ситуации.

**Первая — нормальная.** Например, `project-29-voting-app-argocd`: README на **40 КБ**, это полноценный пошаговый гайд, просто все команды и манифесты вписаны прямо в markdown, копировать нечего. Так же устроены `project-25-petshop-devsecops` (33 КБ) и `project-16-jenkins-argocd-k8s` (29 КБ).

**Вторая — пустышка.** README на 500–1000 байт, вся суть — ссылка «подробный гайд в блоге»:

| Проект | README | Ссылка на гайд |
| :--- | ---: | :--- |
| `project-14-github-actions-android` | 527 б | ❌ 404 |
| `project-36-aws-realtime-deployment` | 794 б | ❌ 404 |
| `project-13-zomato-clone-devsecops` | 972 б | ❌ 404 |
| `project-12-super-mario-k8s` | 1035 б | ❌ 404 |
| `project-11-aws-2tier-terraform` | 5260 б | ❌ 404 |
| `project-09-devsecops-netflix-clone` | 34,5 КБ | ❌ 404 |

**Все шесть статей на `devcloudninjas.hashnode.dev` удалены**, хотя корень блога отвечает 200. У `project-12` и `project-13` вдобавок есть строка «Project Source Code» — и она ведёт **обратно в эту же папку с двумя файлами**. То есть проект замкнут сам на себя и пуст.

---

## 🧟 Что уже протухло

Коммит-сообщения обещают «remediate stale Docker images» и «Updated Docker, GitHub Actions, Kubernetes, and Terraform baselines **where safe**». Оговорка «where safe» делает всю работу:

- **Kubernetes:** `cluster_version = "1.29"` (`project-19`) и `"1.27"` (`project-33`). В [календаре поддержки EKS](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html) сейчас перечислены только **1.31–1.36** — обе версии вне даже расширенной поддержки.
- **Trivy:** в `project-30-blog-app-eks` (строки 339–340) команда `wget .../v0.43.0/trivy_0.43.0_Linux-64bit.deb` → **404**, релиз убран. Актуальный — **v0.74.0** (14.08.2026).
- **GitHub Actions:** `actions/checkout@v2` и `@v3` — **12 вхождений** в воркфлоусах проектов.
- **Docker-образы:** `microsoft/dotnet:2.1-sdk-nanoserver-*` (реестр `microsoft/dotnet` давно заменён на `mcr.microsoft.com/dotnet`, .NET Core 2.1 снят с поддержки), `openjdk:8u131-jre`, `node:16`, `node:lts`, `ubuntu:latest`, `python:alpine`, `amazonlinux` вообще без тега. И 12 манифестов с `image: ...:latest`.
- **Мёртвые исходники приложений.** Из 118 github-ссылок в README (не считая явных плейсхолдеров вроде `<your-github-username>`) не отвечают: `MSFaizi/register-app`, `Tahjib75/nodejs-calculator`, `DevOpsCloudNinjas/DEVOPS_JENKINS_101`, `DevOpsCloudNinjas/DevOps_MasterPiece-CD-with-argocd`, `DevOpsCloudNinjas/DevSecOps-project`, `DevOpsCloudNinjas/medicure-project`, `harshhaareddy/eks-cluster-terraform` и 9 картинок-ассетов у `project-11`. Аккаунты **`harshhaareddy`, `apotitech` и `DevOpsCloudNinjas` отдают 404** — а `apotitech` числится автором части коммитов в этом же репозитории.

> [!tip] Что это значит на практике
> CI/CD-лабораторная, у которой репозиторий приложения удалён, не доводится до конца без замены приложения своим. Это нормальный учебный опыт, но к «забрал и закинул в портфолио» отношения не имеет.

---

## 💸 Сколько это стоит (в посте не сказано)

Проверено по официальным прайсам AWS:

| Ресурс | Цена | В месяц (730 ч — расчёт самого AWS) |
| :--- | :--- | :--- |
| **EKS, контрол-плейн, стандартная поддержка** | $0,10 / кластер / час | **≈ $73** |
| **EKS, расширенная поддержка** (старая версия K8s) | $0,60 / кластер / час | **≈ $438** |
| **NAT Gateway** | $0,045 / час + $0,045 / ГБ | **≈ $32,85** + трафик |
| Ноды EC2, ELB, EBS, ECR | сверху | — |

> [!warning] Free Tier тут не спасает
> На [странице цен EKS](https://aws.amazon.com/eks/pricing/) прямым текстом: *«You pay $0.10 per hour for each Amazon EKS cluster that you create»* — никакой бесплатной квоты на кластер нет, счётчик идёт с первого часа. И тут же вторая ловушка: **если поднять кластер на K8s 1.27/1.29 как в репозитории, попадёшь в extended support — $0,60/час, вшестеро дороже.**

13 проектов сам репозиторий помечает `cost_risk: high`: `project-01`, `07`, `15`, `19`, `28`, `30`, `32`, `33`, `37`, `38`, `46`, `47`, `48`.

**А вот 9 проектов с `cost_risk: low` — их можно гонять локально бесплатно:**

| Проект | Статус |
| :--- | :--- |
| `project-40-k8s-dashboard-trivy` | local_demo |
| `project-41-online-boutique-microservices` | local_lab, kubernetes_ready |
| `project-49-text-encryption-cybersecurity` | local_demo |
| `project-50-argocd-gitops-home-lab` | local_lab, kubernetes_ready |
| `project-51-opentelemetry-observability-home-lab` | local_lab, container_ready |
| `project-53-supply-chain-security-lab` | ci_lab |
| `project-54-progressive-delivery-home-lab` | local_lab, kubernetes_ready |
| `project-14-github-actions-android` | ci_lab (но README — 404-ссылка) |
| `project-03-linux-fundamentals` | reference |

Именно с них и стоит начинать — это самые свежие лабораторные (50–54 добавлены в мае 2026) и единственные, которые не требуют платёжной карты.

---

## 🎭 Портфолио: где проходит граница

Пост предлагает «забрать проект и закинуть в портфолио». Репозиторий идёт дальше — в `docs/marketing/index.md` (и на сайте) лежат **готовые посты в LinkedIn, написанные от первого лица**:

> *«I just finished modernizing my DevOps and Cloud Engineering portfolio lab. It includes 54 hands-on projects…»*
>
> *«I built and modernized a multi-project DevOps lab that demonstrates infrastructure as code…»*

Опубликовать такое, ничего не сделав, — это не «портфолио», а заявление о чужой работе. У репозитория **463 форка** с идентичными README; любой рекрутер, который вобьёт название проекта в поиск, увидит и оригинал, и сотни копий. Работает противоположное: взять один локальный проект из списка выше, честно переписать под себя (а переписывать придётся — см. раздел про протухшее), задокументировать что сломалось и как чинил. Ровно это репозиторий и советует в `docs/runbooks/student-implementation-guide.md`.

> [!info] Это верхушка платной воронки
> На сайте опубликованы прайсы:
> - **Premium Kit** — $29 / $49 / $149 (шаблоны README, чек-листы, воркбук). Страница живая, но **кнопки оплаты нет**: в `docs/premium-kit/index.md` прямо написано *«Add the checkout link here only after the product exists»* — то есть продукт ещё не собран.
> - **Accelerator** — $199–$299 (группа), $499–$799 (малая группа), $149–$249 (разбор 1:1).
> - **For schools** — $1 500–$3 500 (когорта), $2 500–$7 500 (корпоративное обучение).
>
> Сами лабораторные при этом остаются бесплатными, и репозиторий это честно оговаривает: *«The public labs remain free»*, *«The Premium Kit should not sell access to other people's code»*.

---

## ⚖️ Лицензии: MIT в корне — но не везде

Бейдж и API GitHub показывают **MIT** (корневой `LICENSE` — MIT © 2026 DevCloudNinjas). Внутри проектов лежат **свои** файлы лицензий, и они другие:

| Проект | Лицензия |
| :--- | :--- |
| `project-38-docker-terraform-3tier` | **AGPL-3.0** |
| `project-39-gha-aws-terraform` | **AGPL-3.0**, © 2022 Harshhaa Reddy |
| `project-32-tetris-devsecops-k8s` | Apache-2.0 |
| `project-42-serverless-api-dynamodb` | Apache-2.0 |
| `project-48-terraform-aws-eks` | MIT © 2022 Harshhaa Reddy |
| `project-44`, `project-45` | MIT © 2023 DevOps Cloud Ninjas |

**AGPL-3.0 — это важно.** Если поднимешь такой проект как сетевой сервис, обязан отдавать исходники пользователям сервиса. Для учебного портфолио на GitHub это обычно не проблема (код и так открыт), но «MIT, делай что хочешь» — неверное описание всего репозитория.

---

## 🔐 Безопасность: два наблюдения

**В плюс.** Заявленная зачистка секретов подтверждается: прогнал по всему дереву — **ни одного ключа вида `AKIA…`**, ни одного зашитого 12-значного AWS Account ID в `.tf`/манифестах/Jenkinsfile. Есть `SECURITY.md`, 6 воркфлоусов CI (в т.ч. OpenSSF Scorecard), и отдельный ранбук `docs/runbooks/credentials-and-cost-safety.md` — толковый: требует свой аккаунт, бюджетные алерты, `terraform destroy` до старта, запрещает коммитить `.env`/`*.tfvars`/kubeconfig и брать чужие ключи из скриншотов.

**В минус.** В `project-44-devsecops-101` лежит **бинарник Jenkins-плагина** `kubernetes-cd.hpi` на **15,7 МБ**. По манифесту внутри: `Plugin-Version: 1.0.0`, `Jenkins-Version: 2.60.3` — сборка под Jenkins 2017 года. Скармливать своему Jenkins бинарь из чужого учебного репозитория вместо установки из официального update-центра — плохая привычка; если плагин нужен, ставь его штатно.

---

## 🧰 Проверка их собственных инструментов (запускал у себя)

В корне есть `Makefile` и валидаторы на Python. Проверил вживую:

```bash
git clone --depth 1 https://github.com/DevCloudNinjas/DevOps-Projects.git
cd DevOps-Projects
python3 -m venv .venv && .venv/bin/pip install -r tools/requirements.txt   # pytest, PyYAML, hypothesis
.venv/bin/python -m tools.list_projects --validate-metadata   # → 54 строки
.venv/bin/python -m tools.quality_gate .                      # → Quality gate passed: no failures found.
```

Работает, метаданные валидны, гейт зелёный. Это про репозиторий, а не про облако: `make validate-project PROJECT=…` проверяет форматирование и структуру, но **не доказывает, что `terraform apply` пройдёт**, — репозиторий и сам это оговаривает.

---

## 🪶 Как забрать это, не выкачивая 757 МБ

Полный клон — **757 МБ**. Если нужны только гайды и метаданные (а в 90 % случаев нужны именно они), берётся разреженный клон:

```bash
git clone --depth 1 --filter=blob:none --no-checkout \
  https://github.com/DevCloudNinjas/DevOps-Projects.git devops-projects
cd devops-projects
git sparse-checkout set --no-cone '/*.md' '/project-*/README.md' '/project-*/project.yaml' '/docs'
git checkout
```

Замерил результат: **3,1 МБ, 146 файлов** вместо 757 МБ. Влезает даже во flash роутера.

Быстрый отбор проектов по метаданным без чтения всего подряд:

```bash
# всё, что не требует облачного счёта
grep -l 'cost_risk: low' project-*/project.yaml
# наоборот, что ударит по кошельку
grep -l 'cost_risk: high' project-*/project.yaml
# пустышки-ссылки
grep -l 'status: reference' project-*/project.yaml
```

---

## 💻 Что ставить под лабораторные (по системам)

Облако тут опционально: `kind`/`minikube` + Docker закрывают все девять `cost_risk: low` проектов.

### Gentoo (основная, сборка из исходников)

```bash
# контейнеры
emerge -av app-containers/docker app-containers/docker-cli   # 29.8.0
rc-update add docker default && rc-service docker start
usermod -aG docker <user>
# kubernetes
emerge -av sys-cluster/kubectl sys-cluster/minikube app-admin/helm sys-cluster/k9scli
# IaC
emerge -av app-admin/opentofu     # 1.10.6, Apache-2.0
```

Полезные USE-флаги `app-containers/docker`: `IUSE="apparmor btrfs +container-init cuda +overlay2 seccomp selinux systemd"`.

> [!warning] Три нюанса Gentoo
> - **`app-admin/terraform` (1.16.1) идёт с `LICENSE="BUSL-1.1"`** — это не OSI-лицензия, придётся принять её в `ACCEPT_LICENSE`. Именно из-за смены лицензии HashiCorp и появился OpenTofu; в репозитории для этого даже есть отдельный `project-52-opentofu-aws-free-tier-lab`. Бери `app-admin/opentofu` — он Apache-2.0 и совместим по синтаксису.
> - **`kind` в ::gentoo отсутствует.** Либо `sys-cluster/minikube` (есть, 1.38.1, с USE `libvirt`), либо ставь kind через `go install sigs.k8s.io/kind@latest`.
> - **AWS CLI:** `app-admin/awscli` — это **линейка v1** (1.46.1), собирается из исходников. Версия v2 существует только как `app-admin/awscli-bin` (2.36.34) — бинарь, потому что апстрим v2 исходников для сборки не отдаёт. Для лабораторных v1 хватает.

### Debian / Ubuntu

Версии в репозиториях (проверено по Debian madison):

| Пакет | stable | testing/unstable |
| :--- | :--- | :--- |
| `docker.io` | 26.1.5 | 28.5.2 |
| `kubernetes-client` (даёт `kubectl`) | 1.32.3 | 1.33.4 |
| `helm` | 4.0.3 | 4.0.7 |
| `awscli` (v2) | 2.23.6 | 2.36.17 |
| `podman` | 5.4.2 | 5.8.6 |
| **`terraform`** | **нет в репозиториях** | **нет** |
| **`opentofu`** | **нет в репозиториях** | **нет** |

```bash
sudo apt install docker.io kubernetes-client helm awscli
sudo usermod -aG docker $USER
# OpenTofu — официальным установщиком
curl -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh
chmod +x install-opentofu.sh && ./install-opentofu.sh --install-method deb
# kind — бинарь с GitHub (в apt его нет)
```

Terraform в Debian нет ровно по той же причине — BUSL-1.1; ставится либо из apt-репозитория HashiCorp, либо, что здоровее, заменяется на OpenTofu.

### Arch (с июня 2026)

Всё есть в официальных репозиториях, ничего из AUR не нужно:

```bash
sudo pacman -S docker kubectl helm kind minikube opentofu aws-cli-v2 k9s
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

| Пакет | Версия |
| :--- | :--- |
| `extra/docker` | 29.7.2 |
| `extra/kubectl` | 1.36.4 |
| `extra/helm` | 4.2.2 |
| `extra/kind` | 0.33.0 |
| `extra/minikube` | 1.38.1 |
| `extra/opentofu` | 1.12.1 |
| `extra/terraform` | 1.15.9 (BUSL, если всё же нужен) |
| `extra/aws-cli-v2` | 2.34.32 |
| `extra/k9s` | 0.51.0 |

### Entware / ASUS RT-AX56U (armv7, 512 МБ RAM, 256 МБ flash)

❌ **Запускать нечего.** Прошёлся подстрочным поиском по всем **3026 пакетам** ветки `armv7sf-k3.2`: нет ни `docker`, ни `kube*`, ни `terraform`, ни `tofu`, ни `helm`, ни `aws*`. Да и 512 МБ RAM для kubelet физически мало.

✅ Что роутер **может** — работать читалкой и зеркалом:

```bash
opkg install git git-http jq
cd /opt/share/usb   # обязательно на USB-диск, не во flash
git clone --depth 1 --filter=blob:none --no-checkout \
  https://github.com/DevCloudNinjas/DevOps-Projects.git
```

Полный клон (757 МБ) в 256 МБ flash не влезет физически; разреженный (3,1 МБ) влезет куда угодно. Плюс `jq` пригодится для разбора `project.schema.json`.

---

## 🎯 Итог

| | |
| :--- | :--- |
| **Что правда** | 54 проекта; действительно большой массив материалов; машиночитаемые метаданные с честной пометкой стоимости и статуса; живой сайт-портал; работающий локальный quality gate; толковый ранбук по безопасности и деньгам; секреты вычищены |
| **Что не так в посте** | «Любой проект» — 10 из 54 пустые, 6 гайдов удалены (404); «и другим подтемам» — это на 88 % AWS; про деньги и про то, что почти всё требует обновления, не сказано ни слова |
| **Главный подвох** | Не техника, а этика: репозиторий раздаёт готовые посты в LinkedIn от первого лица к чужой работе, разошедшейся в 463 форка |
| **Как пользоваться** | Разреженный клон (3,1 МБ) → `grep -l 'cost_risk: low'` → взять 1–2 проекта из `project-50…54` → поднять локально в kind/minikube → переписать под себя → в портфолио идёт **твой** репозиторий с твоим разбором граблей |

Как учебный материал — годится, если относиться к нему как к **сборнику чужих статей с неровным качеством**, а не как к курсу. Как «готовое портфолио» — не годится ни технически, ни по-человечески.

---

## 🔗 Связанные заметки

- Каталог бесплатных курсов с сертификатами — тот же жанр, тоже с оговорками: [awesome-certificates (PanXProject)](awesome-certificates%20%28PanXProject%29%20%E2%80%94%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20200%2B%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D1%85%20%D0%BA%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D1%81%20%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%D0%BC%D0%B8%20%28IT-CS-%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81%29%2C%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B.md)
- Системный самоучитель по Computer Science: [CS Self-learning (CSDIY)](CS%20Self-learning%20%28CSDIY%2C%20csdiy.wiki%29%20%E2%80%94%20%D0%B3%D0%B8%D0%B4%20%D0%BF%D0%BE%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%BC%D1%83%20%D0%B8%D0%B7%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8E%20Computer%20Science%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D0%B0%D0%BC%20%D1%82%D0%BE%D0%BF-%D0%B2%D1%83%D0%B7%D0%BE%D0%B2.md)
- Ещё одна подборка, где часть «курсов» оказалась не курсами: [robotics-coursework (mithi)](robotics-coursework%20%28mithi%29%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%BA%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D0%BF%D0%BE%20%D1%80%D0%BE%D0%B1%D0%BE%D1%82%D0%BE%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20152%20%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B8%2C%20%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D1%83%209%20%D0%BB%D0%B5%D1%82%2C%20%D1%87%D0%B0%D1%81%D1%82%D1%8C%20%C2%AB%D0%BA%D1%83%D1%80%D1%81%D0%BE%D0%B2%C2%BB%20%D1%8D%D1%82%D0%BE%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B0%20%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0%29.md)
- Сканер безопасности Docker-образов — пригодится в DevSecOps-лабораторных: [DockerScan (cr0hn)](../Security/Vulns/Linux/DockerScan%20%28cr0hn%29%20%E2%80%94%20%D1%81%D0%BA%D0%B0%D0%BD%D0%B5%D1%80%20%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20Docker-%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%20%D0%BD%D0%B0%20Go%20%28CIS%2C%20%D1%81%D0%B5%D0%BA%D1%80%D0%B5%D1%82%D1%8B%2C%20CVE%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%B8.md)
- Подготовка к техническим собеседованиям: [19 паттернов алгоритмических задач (ByteByteGo)](../Programming/Algorithm/19%20%D0%BF%D0%B0%D1%82%D1%82%D0%B5%D1%80%D0%BD%D0%BE%D0%B2%20%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%D0%B4%D0%BB%D1%8F%20%D1%81%D0%BE%D0%B1%D0%B5%D1%81%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B9%20%28ByteByteGo%20Coding%20Patterns%29%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D1%83%D1%87%D0%B8%D1%82%D1%8C%20%D0%B8%20%D0%B3%D0%B4%D0%B5%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE.md)

## 🔗 Ссылки

- Репозиторий: [github.com/DevCloudNinjas/DevOps-Projects](https://github.com/DevCloudNinjas/DevOps-Projects) (MIT в корне, AGPL/Apache внутри) · Портал: [devcloudninjas.github.io/DevOps-Projects](https://devcloudninjas.github.io/DevOps-Projects/)
- Каталог проектов: [PROJECTS.md](https://github.com/DevCloudNinjas/DevOps-Projects/blob/master/PROJECTS.md) · Ранбук по деньгам и ключам: [credentials-and-cost-safety](https://devcloudninjas.github.io/DevOps-Projects/runbooks/credentials-and-cost-safety/)
- Цены AWS: [EKS pricing](https://aws.amazon.com/eks/pricing/) · [VPC/NAT pricing](https://aws.amazon.com/vpc/pricing/) · [Календарь версий Kubernetes в EKS](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html)
- OpenTofu: [opentofu.org](https://opentofu.org/) · kind: [kind.sigs.k8s.io](https://kind.sigs.k8s.io/)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/27570)

#DevOps #Kubernetes #Terraform #AWS #CI-CD #DevSecOps #Подборка #Карьера
