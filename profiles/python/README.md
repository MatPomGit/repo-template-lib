# Python / PyPI (opcjonalne)

Użyj `pyproject.toml` z PEP 517/518, właściwym `name`, zależnościami, licencją i testami instalacji wheel/sdist w pustym venv.
Sprawdź `python -m build`, `pip install dist/*.whl`, import i API test.
GitHub Packages **nie oferuje natywnego indeksu PyPI**. Wheel można dołączyć do GitHub Releases; publikacja PyPI wymaga osobnej decyzji.
