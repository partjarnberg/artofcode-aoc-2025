# 2025 · dag 1 · agent

[Uppgiften: Secret Entrance](https://adventofcode.com/2025/day/1). Lösningen skrevs med Codex i Python utan externa paket. Python 3.9 eller senare fungerar; Docker och CI använder Python 3.13. Båda delarna godkändes hos AoC den 10 november 2026.

## Kör från repots rot

Spara dina egna indata lokalt i `.private/inputs/2025-01.txt`. Mappen ignoreras av Git och Docker. Publicera inte indata eller uppgiftstext.

```sh
python3 days/01/agent/src/solve.py --part 1 < .private/inputs/2025-01.txt
python3 days/01/agent/src/solve.py --part 2 < .private/inputs/2025-01.txt
python3 -m unittest discover -s days/01/agent/tests -v
```

Programmet läser stdin radvis och skriver ett heltal till stdout. Ogiltiga rotationer ger ett fel med radnummer på stderr och exitkod 2.

## Docker gör lösningen enkel att prova

Dockerfile paketerar Python, kopierar kod och egna tester och kör testerna under bygget. Programmet startar sedan utan root-rättigheter. Andra kan prova samma lösning utan att installera Python lokalt. Indata skickas in vid körning och finns inte i imagen.

```sh
docker build -f days/01/agent/Dockerfile -t advent-2025-day01-agent .
docker run --rm -i advent-2025-day01-agent --part 1 < .private/inputs/2025-01.txt
docker run --rm -i advent-2025-day01-agent --part 2 < .private/inputs/2025-01.txt
```

Workflow **Verify solutions** bygger containern, kör testerna och provar båda CLI-svaren med egna små data vid ändringar. ART of Codes server gör statisk analys efter att AoC har godkänt respektive del. Den kör inte Docker och mäter ingen exekveringstid. Ingen `solution.json` behövs: koden ligger i standardmappen `src/`.

## Idén och fallgropen

Positionen hålls modulo 100. Del 1 räknar rotationer som slutar på noll. Del 2 räknar varje klick som når noll, även mitt i en rotation. `divmod` delar avståndet i hela varv och återstående klick: varje helt varv ger ett nollbesök, och resten kan ge högst ett till.

Att börja på noll och vrida åt vänster är den viktiga gränsen: startpositionen ska inte räknas som ett nytt besök. Därför kontrollerar vänsterfallet `0 < position <= remainder`.

Vi går igenom varje rad en gång och sparar bara räknare och aktuell rad. Antalet beräkningssteg per rotation växer inte med antalet klick; stora heltal har dock sin vanliga aritmetiska kostnad.

## Verifiera och vidareutveckla

De tio testerna använder egna data och en oberoende simulering som vrider ett klick i taget. De provar alla startpositioner nära varvgränser, 200 deterministiska slumpsekvenser, stora tal, tomma rader, felaktig indata och CLI:t. Även den privata indatafilens resultat jämfördes lokalt med simuleringen.

Ändra koden, lägg till ett test för ditt nya fall och kör testerna samt Dockerbygget. Pusha sedan till `main`; publiceringsworkflowet registrerar den nya kodversionen för analys. [Checklistan för färdig analys](https://aoc.artofcode.se/startrepot/#fardig-analys) förklarar väntan på AoC och hur resultatet syns.

## Hur agenten användes

Codex skrev lösning, tester, container och dokumentation i en interaktiv session. Pär valde uppgift, tillhandahöll indata och godkände användningen av sin inloggade webbläsare för inlämningen. Det här är en agentassisterad lösning; repot innehåller ännu inget fristående system som själv hämtar uppgifter och skickar svar. Se [arbetsinstruktionen](../../../agent/instructions/day01.md).

`run.json` redovisar verktyget Codex. Exakt modell-ID och anropsstatistik är inte tillgängliga i denna körning, så modellistan är tom och okända tal är `null`. Det betyder okänd modellanvändning, inte att lösningen skrevs utan AI.
