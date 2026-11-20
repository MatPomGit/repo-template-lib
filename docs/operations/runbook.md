# Runbook uruchomienia i wydania biblioteki

**Stan: NOT_CONFIGURED.** Szablon nie ma produkcyjnego runtime, pakietu ani aktywnego wsparcia.

Po pierwszej implementacji zapisz zweryfikowane polecenia budowania, instalacji w czystym środowisku, testów API, diagnostyki, rollbacku i odtwarzania wersji. Opisz SHA źródeł, narzędzia, lockfile, hash wynikowego artefaktu i uprawnienia. Bez sekretów, prywatnych logów i rzeczywistych danych osób badanych.

Rozdziel: walidację statyczną, build, test artefaktu, wydanie, publikację do registry i instalację konsumenta. Każdy etap ma własne dowody. `NOT_RUN` i `NOT_RELEASED` nie oznaczają `PASS`.

Zobacz [instalację](../installation.md), [release](../releases.md), [kompatybilność](../compatibility.md) i [supply-chain](../security/supply-chain.md).
