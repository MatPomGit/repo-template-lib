# Polityka GitHub Actions

Szablon celowo nie zawiera automatycznie aktywowanych workflowów.
Domyślny tryb walidacji: `python scripts/validate_repository.py --phase scaffold` i lokalne `unittest`.
Przed dodaniem CI sprawdzić limity, uprawnienia, dostępność disposable runners i zgodę właściciela.
Nigdy nie wykonywać kodu niezaufanych PR na stałych runnerach HomeServer/Andromeda.
Wydania pakietów i publikacja Pages to odrębne, kontrolowane operacje.
