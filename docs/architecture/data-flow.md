# Przepływy danych i granice zaufania

**Stan: NOT_ASSESSED.** Szablon nie wykonuje produkcyjnego przetwarzania.

Dla każdego zaimplementowanego przepływu zapisz źródło (API, plik, sieć, urządzenie), typ i jednostkę, walidację danych, granice zaufania, transport, serializację, uprawnienia, odbiorcę i retencję. Rozróżniaj dane syntetyczne, pomiar rzeczywisty i zweryfikowany sprzętowo.

Nie wnioskuj o bezpieczeństwie tylko z istnienia schematu API. Każda nowa integracja wymaga dowodu testowego i aktualizacji [modelu zagrożeń](../security/threat-model.md). Dane osób badanych i sekrety pozostają poza publicznym repo oraz Pages.

Źródła: [API](../contracts.md), [prywatność](../privacy.md), [ADR](../adr/0002-security-boundaries.md).
