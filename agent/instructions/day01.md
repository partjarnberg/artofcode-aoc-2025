# Arbetsinstruktion · 2025 dag 1

Ge instruktionen till ditt kodverktyg från repots rot. Inga modellnycklar behövs för att köra den färdiga Python-lösningen.

1. Läs uppgiften på <https://adventofcode.com/2025/day/1> med deltagarens godkända åtkomst. Personlig indata ligger i `.private/inputs/2025-01.txt` och får aldrig publiceras.
2. Läs repots körkontrakt. Skriv eller förbättra `days/01/agent/src/solve.py` med stdin, `--part 1|2` och ett heltal på stdout.
3. Räkna hela varv och en återstod. Testa särskilt vänstervridning från noll och flera hela varv.
4. Jämför med en separat klicksimulering och egna deterministiska testdata. Kör `python3 -m unittest discover -s days/01/agent/tests -v` och Dockerbygget enligt dagens README.
5. Kör personliga indata bara lokalt. Låt deltagaren styra eventuell inlämning till AoC, respektera väntetider och gör inga gissningsloopar.
6. Uppdatera dokumentation och eventuell modellrapport med faktisk metadata. Gissa inte modell-ID eller tokenantal.
7. Kontrollera diffen och pusha när deltagaren bett om det. GitHub Actions registrerar kodversionen. Tjänstens ordinarie AoC-synk avgör när analysen får starta.

Vid avbrott: läs dagens README och senaste commit, kontrollera vad som redan är godkänt och kör testerna innan du fortsätter. Ett nästa steg är en verktygsadapter som hämtar verkliga modell-ID:n och tokenantal från agentens API-svar till `run.json`.
