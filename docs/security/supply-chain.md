# Bezpieczeństwo łańcucha dostaw

**Stan: NOT_CONFIGURED.** Nie istnieje gotowy pakiet ani realny rejestr zależności.

Po wyborze ekosystemu dokumentuj wszystkie zależności bezpośrednie i przechodnie, ich źródła, licencje, wersje, artefakty i uzasadnione wyjątki. Użyj lockfile i weryfikacji integralności adekwatnej do npm, Maven, NuGet, Pythona, Unity UPM lub OCI. Jeżeli transitive lock jest niemożliwy, opisz ograniczenie.

Przed wydaniem sprawdź prawdziwe wyniki skanu podatności i licencji, pochodzenie materiałów, integralność i hash artefaktu, uprawnienia registry i clean install. Sekrety publikacyjne nigdy nie mogą trafiać do niezaufanych PR.

Powiązania: [zależności](../dependencies.md), [ADR](../adr/0003-supply-chain.md), [wydania](../releases.md).
