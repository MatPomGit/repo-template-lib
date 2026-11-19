# Zależności i łańcuch dostaw

Zapisz każdy runtime, SDK, manager pakietów, licencję, pakiet i przypiętą wersję/SHA/digest. Plik blokady odpowiedni do platformy jest częścią projektu produkcyjnego.
Repozytoria prywatne i Github Packages mają odrębne reguły uwierzytelniania. Dostęp GitHub App do kodu nie oznacza automatycznego dostępu do prywatnych pakietów.
Repozytoria nadrzędne `arc-*` powinny odczytywać zdalny HEAD każdej zależności w trybie audytu bieżącego, ale odtwarzać badanie `msc-*` na historycznie przypiętych wersjach.
Wymagana osobna weryfikacja licencji SDK, modeli i assetów, także Unity oraz rozszerzeń natywnych.
