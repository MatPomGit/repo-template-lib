# Instrukcje dla agentów: repozytorium `lib-*`

Najpierw przeczytaj `PROJECT_STATE.yaml`, `config/component.json`, `ARCHITECTURE.md`, `SECURITY.md`, kontrakty i lokalną politykę Actions.
Ten szablon dotyczy biblioteki, a nie domyślnie pracy naukowej `msc-*`.

1. Odczytuj aktualny stan repozytorium, otwarte PR, datę i commit SHA. Historyczny submoduł ani lockfile nie są najnowszą wersją źródła.
2. Nie wykonuj automatycznie kodu z niezaufanych gałęzi na stałych runnerach; najpierw testuj offline i w odizolowanym środowisku.
3. Jeden komponent = jeden właściciel źródeł. Nie kopiuj kodu między `msc-*`, `app-*`, `lib-*`.
4. Respektuj `contracts/`, status kompatybilności i identyfikatory z Research Autopilot. Nie fabrykuj pomiarów sprzętowych.
5. Rozdziel stany: zaplanowane, zaimplementowane, testowane, wydane, wdrożone i zwalidowane na urządzeniu.
6. Aktualizacja biblioteki lub pakietu nie zmienia automatycznie reprodukowalnego snapshotu użytego w `msc-*`.
7. Zachowuj blokadę wydania do czasu licencji, testów, weryfikacji zależności i zgody właściciela.
8. Zero-spend, minimalne uprawnienia, brak publikacji/secrets/host changes bez zgody. Polityka WIP Research Autopilot obowiązuje.
