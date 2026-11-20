# Reguły profilu OCI

Ta instrukcja jest lokalnym rozszerzeniem głównych [AGENTS.md](../../AGENTS.md). Nie osłabia bramek R0–R3 ani nie nadaje prawa publikacji.

Biblioteka jako obraz OCI: używaj przypiętych digest bazowych, minimalnych warstw i uprawnień, kontroli SBOM oraz manifestu architektur. Zbudowany kontener nie jest wdrożeniem. Nie dawaj niezaufanemu PR dostępu do Docker socket hosta i prywatnego registry; kontroluj skan obrazu, checksum i decyzję o publikacji.

Przy pierwszym rzeczywistym module uzupełnij [kontrakty](../../docs/contracts.md), [kompatybilność](../../docs/compatibility.md), [architekturę](../../docs/architecture/README.md) i [ryzyko zależności](../../docs/security/supply-chain.md). Każdy wynik testowy podawaj z dokładnym SHA i środowiskiem, a brak testu jako `NOT_RUN`. Materiały publiczne należą wyłącznie do `pages/`, nie do wewnętrznych instrukcji.
