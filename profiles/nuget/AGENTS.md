# Reguły profilu NUGET

Ta instrukcja jest lokalnym rozszerzeniem głównych [AGENTS.md](../../AGENTS.md). Nie osłabia bramek R0–R3 ani nie nadaje prawa publikacji.

Biblioteka .NET/NuGet: ustaw target frameworks, publiczne API, kompatybilność binarną, strong name (jeśli właściwe), metadane licencji i zależności. Testuj restore/build/package w izolacji oraz zainstalowanie .nupkg w przykładowym konsumencie. Publikacja registry i podpisy są osobną bramką.

Przy pierwszym rzeczywistym module uzupełnij [kontrakty](../../docs/contracts.md), [kompatybilność](../../docs/compatibility.md), [architekturę](../../docs/architecture/README.md) i [ryzyko zależności](../../docs/security/supply-chain.md). Każdy wynik testowy podawaj z dokładnym SHA i środowiskiem, a brak testu jako `NOT_RUN`. Materiały publiczne należą wyłącznie do `pages/`, nie do wewnętrznych instrukcji.
