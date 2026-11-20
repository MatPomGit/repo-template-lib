# ADR-0002: granice zaufania biblioteki

**Status:** proposed  
**Data:** 2026-11-20

## Kontekst

Biblioteka może wykonywać kod w różnych środowiskach i przetwarzać niezaufane wejścia, pliki oraz dane urządzeń. Nie ma jeszcze zdefiniowanego runtime ani faktycznych uprawnień.

## Propozycja

Waliduj wejścia z granic API, plików, transportu i urządzeń. Ogranicz uprawnienia, izoluj kod niezaufanych PR, przechowuj sekrety poza repo i artefaktami. Nie zapisuj prywatnych pomiarów w publicznym Pages ani logach.

## Alternatywy i konsekwencje

Biblioteka wyłącznie offline, SDK urządzeniowe, lokalny proces lub usługa sieciowa różnią się powierzchnią ataku. Przy wdrożeniu wybierz konkretne kontrole i dowody testowe w [modelu zagrożeń](../security/threat-model.md). Propozycja nie jest pozytywnym audytem.
