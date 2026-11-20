# Bezpieczeństwo biblioteki

**Status: CONTACT_NOT_CONFIGURED.** Szablon nie ma aktywnego prywatnego kanału przyjmowania zgłoszeń. Przed wydaniem wskaż i sprawdź rzeczywisty kontakt; `REPLACE_CONTACT` nie jest działającym adresem ani obietnicą reakcji.

Nie publikuj exploitów, sekretów, danych uczestników, prywatnych logów i tokenów w publicznych Issues. Zgłoszenie podatności powinno zawierać wersję i SHA, minimalną reprodukcję oraz zakres wpływu, przekazane prywatnie upoważnionemu właścicielowi.

Kod niezaufanych PR i SDK uruchamiaj tylko w izolacji, bez praw do stałych runnerów, Docker socket, produkcyjnych baz i sekretów. Aktualizacje zależności przechodnich, licencje, manifest pakietu, podatności i hashe podlegają weryfikacji przed release. `NOT_RUN` i `NOT_VERIFIED` nie są `PASS`. Nie przesyłaj telemetrii ani danych badawczych bez jawnego kontraktu.

Zobacz [model zagrożeń](docs/security/threat-model.md), [łańcuch dostaw](docs/security/supply-chain.md), [obsługę incydentów](docs/security/incident-response.md) oraz [politykę Pages](docs/pages.md). Publikacja pakietu i witryny wymaga niezależnej, właściwie zatwierdzonej decyzji.
