# Reguły profilu UNITY

Ta instrukcja jest lokalnym rozszerzeniem głównych [AGENTS.md](../../AGENTS.md). Nie osłabia bramek R0–R3 ani nie nadaje prawa publikacji.

Biblioteka Unity UPM: właściwy układ Runtime/Editor/Tests/Samples~/Documentation~, package.json i asmdef, rozdziel platformy i URP/HDRP. Testuj import w czystym projekcie, właściwą wersję Unity, kompilację, kompatybilność i rzeczywisty sprzęt, jeśli dotyczy. Nie utożsamiaj builda ze zweryfikowanym działaniem na urządzeniu. Zależności Git u odbiorcy przypinaj przez manifest/lockfile.

Przy pierwszym rzeczywistym module uzupełnij [kontrakty](../../docs/contracts.md), [kompatybilność](../../docs/compatibility.md), [architekturę](../../docs/architecture/README.md) i [ryzyko zależności](../../docs/security/supply-chain.md). Każdy wynik testowy podawaj z dokładnym SHA i środowiskiem, a brak testu jako `NOT_RUN`. Materiały publiczne należą wyłącznie do `pages/`, nie do wewnętrznych instrukcji.
