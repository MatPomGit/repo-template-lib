# ADR-0003: weryfikacja zależności i artefaktów

**Status:** proposed  
**Data:** 2026-11-20

## Kontekst

Odbiorcy biblioteki wymagają reprodukowalnych wydań, pochodzenia SDK i zgodności licencji. Luźne zależności mogą zmieniać zachowanie bez aktualizacji źródła.

## Propozycja

Zależności przypinaj wersją, lockfile lub SHA/digest według ekosystemu. Przed wydaniem sprawdzaj zależności bezpośrednie i przechodnie, licencje, podatności, integralność artefaktu i realne testy clean install. Statyczny release gate nie jest niezależną atestacją.

## Alternatywy i konsekwencje

Nieograniczone aktualizacje zmniejszają koszt początkowy, lecz osłabiają odtwarzalność. Wybór mechanizmu kontroli wymaga konkretnego runtime i registry. Szczegóły: [supply-chain](../security/supply-chain.md).
