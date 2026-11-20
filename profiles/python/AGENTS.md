# Reguły profilu PYTHON

Ta instrukcja jest lokalnym rozszerzeniem głównych [AGENTS.md](../../AGENTS.md). Nie osłabia bramek R0–R3 ani nie nadaje prawa publikacji.

Biblioteka Python: źródłem konfiguracji pakietu jest `pyproject.toml` z PEP 517/518. Testuj budowanie wheel/sdist, clean install w pustym venv, import i publiczne API. Zadeklaruj wersję Pythona, licencje, transitive dependencies i lock/constraints. Nie zakładaj, że GitHub Packages jest indeksem PyPI. Publikacja PyPI lub GitHub Releases wymaga osobnej zgody.

Przy pierwszym rzeczywistym module uzupełnij [kontrakty](../../docs/contracts.md), [kompatybilność](../../docs/compatibility.md), [architekturę](../../docs/architecture/README.md) i [ryzyko zależności](../../docs/security/supply-chain.md). Każdy wynik testowy podawaj z dokładnym SHA i środowiskiem, a brak testu jako `NOT_RUN`. Materiały publiczne należą wyłącznie do `pages/`, nie do wewnętrznych instrukcji.
