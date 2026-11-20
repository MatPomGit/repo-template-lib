# Reguły profilu NPM

Ta instrukcja jest lokalnym rozszerzeniem głównych [AGENTS.md](../../AGENTS.md). Nie osłabia bramek R0–R3 ani nie nadaje prawa publikacji.

Biblioteka npm: publiczne API jest jawne w exports/types, SemVer i package.json. Lockfile, testy kompatybilności Node/browser, testy ESM/CJS oraz supply-chain muszą odpowiadać faktycznym konsumentom. Nie publikuj paczki automatycznie z CI; sprawdź tokeny, integralność tarball i licencje.

Przy pierwszym rzeczywistym module uzupełnij [kontrakty](../../docs/contracts.md), [kompatybilność](../../docs/compatibility.md), [architekturę](../../docs/architecture/README.md) i [ryzyko zależności](../../docs/security/supply-chain.md). Każdy wynik testowy podawaj z dokładnym SHA i środowiskiem, a brak testu jako `NOT_RUN`. Materiały publiczne należą wyłącznie do `pages/`, nie do wewnętrznych instrukcji.
