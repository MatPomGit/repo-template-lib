# Testy i dowody

Minimalna hierarchia: walidacja szkieletu, testy jednostkowe, testy kontraktowe, test integracji, czysta instalacja i test docelowego środowiska.
Nie wolno wnioskować o poprawnym działaniu urządzenia z testów syntetycznych lub emulatora.
Każdy raport powinien zawierać środowisko, wersje, commit SHA, parametry, wynik, ograniczenia i identyfikator artefaktu. `NOT_RUN` jest poprawnym statusem, nie błędem logicznym.
Test na stałym runnerze nie może wykonywać niezaufanego PR. Rozszerzenie CI wymaga odrębnej zgody i weryfikacji kosztów.
