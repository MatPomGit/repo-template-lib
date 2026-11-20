# Reguły profilu MAVEN

Ta instrukcja jest lokalnym rozszerzeniem głównych [AGENTS.md](../../AGENTS.md). Nie osłabia bramek R0–R3 ani nie nadaje prawa publikacji.

Biblioteka Maven: rozdziel API od kompatybilności binarnej ABI. Dokumentuj JDK, groupId/artifactId, POM, transitive dependencies, licencje i testy instalacji w czystym cache. Zmiana publicznych klas/metod wymaga testu odbiorców. Release do Maven Central/GitHub Packages to osobna czynność z uprawnieniami.

Przy pierwszym rzeczywistym module uzupełnij [kontrakty](../../docs/contracts.md), [kompatybilność](../../docs/compatibility.md), [architekturę](../../docs/architecture/README.md) i [ryzyko zależności](../../docs/security/supply-chain.md). Każdy wynik testowy podawaj z dokładnym SHA i środowiskiem, a brak testu jako `NOT_RUN`. Materiały publiczne należą wyłącznie do `pages/`, nie do wewnętrznych instrukcji.
