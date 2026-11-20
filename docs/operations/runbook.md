# Runbook uruchomienia i wydania biblioteki

**Stan: NOT_CONFIGURED.** Szablon nie ma produkcyjnego runtime, pakietu ani aktywnego wsparcia.

Po pierwszej implementacji zapisz zweryfikowane polecenia budowania, instalacji w czystym środowisku, testów API, diagnostyki, rollbacku i odtwarzania wersji. Opisz SHA źródeł, narzędzia, lockfile, hash wynikowego artefaktu i uprawnienia. Bez sekretów, prywatnych logów i rzeczywistych danych osób badanych.

Rozdziel: walidację statyczną, build, test artefaktu, wydanie, publikację do registry i instalację konsumenta. Każdy etap ma własne dowody. `NOT_RUN` i `NOT_RELEASED` nie oznaczają `PASS`.

Zobacz [instalację](../installation.md), [release](../releases.md), [kompatybilność](../compatibility.md) i [supply-chain](../security/supply-chain.md).

## Administracyjna bramka `main`

Stan stwierdzony 2026-11-20: aktywny ruleset `27652859` zawierał jedynie `deletion` i `non_fast_forward` oraz `bypass_mode: always`. Nie wymuszał zatwierdzonego PR ani obowiązkowego CI. Dokumentacja i zielone testy nie zmieniają konfiguracji GitHub.

Przed wydaniem wymagaj `Require a pull request before merging`, niezależnego `APPROVED` i `Require status checks to pass` dla sprawdzonego joba `validate` (workflow `Scaffold CI`). Ustal poprawną tożsamość źródła checka, ogranicz bypass i bezpośrednie zapisy do `main` oraz przetestuj odmowę merge bez recenzji. W repo prywatnym `validate` może być pominięty; zapewnij uprawnioną kontrolę exact SHA zamiast traktować `SKIPPED` jako dowód. Do czasu faktycznego wdrożenia bramki obowiązuje `GATE_UNENFORCED / HOLD`.
