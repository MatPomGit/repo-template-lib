# Model zagrożeń biblioteki

**Status: NOT_ASSESSED.** Lista pytań nie stanowi potwierdzonej oceny.

| Obszar | Ryzyko | Weryfikacja |
| --- | --- | --- |
| Publiczne API | Niepoprawne wejścia, błędy typów i jednostek | Walidacja i testy negatywne |
| SDK i zależności | Podmiana, podatności, konflikty licencji | Pinned versions, audyt, SBOM |
| I/O i transport | Ujawnienie danych, nadmierny dostęp | Minimalne uprawnienia, testy |
| Aparatura | Niezgodny SDK, błędy interpretacji | Kontrakt sprzętu, test fizyczny |
| Registry i release | Fałszywy artefakt, brak integralności | SHA, hash, izolowany build |
| GitHub Pages | Publikacja `docs/`, promptów i sekretów | Osobne `pages/`, allowlista i review |

Po rozpoczęciu implementacji zapisz aktywa, granice zaufania, scenariusz, prawdopodobieństwo, skutek, kontrolę, dowód i ryzyko rezydualne. Nie deklaruj testu `PASS`, gdy nie był wykonany.

Zobacz [SECURITY](../../SECURITY.md), [przepływy](../architecture/data-flow.md), [łańcuch dostaw](supply-chain.md).
