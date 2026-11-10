# 2025 dag 1 · hantverksexempel

Läs originaluppgiften hos [Advent of Code](https://adventofcode.com/2025/day/1). Den här katalogen innehåller lösningsidéer och är därför en spoiler. Inga AoC-indata eller uppgiftstexter har kopierats hit.

Detta är ett AI-assisterat undervisningsexempel, inte en tävlingsinlämning. Det visar ett tydligt, explicit angreppssätt för hantverksspåret; det är inte påstått handskrivet av en deltagare. Båda delarna stöds. Lösningen har lokala tester, men är inte verifierad med en deltagares privata input eller ett godkännande från AoC.

## Varför finns Dockerfile?

Den paketerar Python 3.13, lösningen och testerna så att någon annan kan klona repot och testköra utan en lokal Python-installation. Docker behöver vara installerat. Att beskriva och förstå körmiljön är en del av hantverksövningen.

- `FROM` väljer körmiljö, `WORKDIR` arbetskatalog och `COPY` tar med koden och våra egna tester.
- `RUN` kör testerna under bygget. Ett misslyckat test stoppar bygget.
- `USER` kör det färdiga programmet som en användare utan root-behörighet.
- `ENTRYPOINT` startar lösningen. `--part` väljer del och stdin levererar indata vid körning.

`.private/` utesluts av repots `.dockerignore`. Personliga AoC-indata ska varken ligga i imagen eller Git. Vår server läser koden statiskt; den bygger eller kör inte denna Dockerfile och mäter ingen exekveringstid. Dockerfile redovisas som infrastruktur, separat från lösningens kodrader.

## Prova utan privata AoC-indata

Bygg från repots rot. Följande rotationer är våra egna små testdata:

```sh
docker build -f examples/2025/day01/manual/Dockerfile -t advent-example-manual .
printf 'R250\nL200\nR1\nL1\n' | docker run --rm -i advent-example-manual --part 1
# Förväntat svar: 3
printf 'R250\nL200\nR1\nL1\n' | docker run --rm -i advent-example-manual --part 2
# Förväntat svar: 6
```

GitHub Actions kör samma bygg- och CLI-kontroll för exemplet. När du ändrar koden bygger du imagen igen för att köra den nya versionen och testerna.

## Kör med egna AoC-indata eller lokal Python

```sh
python3 -m unittest discover -s examples/2025/day01/manual/tests
python3 examples/2025/day01/manual/src/solve.py --part 1 < .private/inputs/2025-01.txt
docker build -f examples/2025/day01/manual/Dockerfile -t advent-example-manual .
docker run --rm -i advent-example-manual --part 2 < .private/inputs/2025-01.txt
```

Testerna skapar egna data och jämför med en oberoende simulering av varje klick. De täcker flera varv, start på noll, tomma rader och felaktiga kommandon. Algoritmen utför konstant arbete per rotation och behöver inte skapa en lista över alla klick.

## Experimentera med exekveringstid

Efter bygget kan du prova `time docker run --rm -i advent-example-manual --part 2 < .private/inputs/2025-01.txt`. Tiden omfattar även container- och Python-start. Det är ett lokalt experiment, inte en mätning som skickas till topplistan. Jämför förbättringar med samma data och miljö, kör flera gånger och håll byggtid separat. En gemensam prestandamätning kräver också en kontrollerad körmiljö; Dockerfile ensam gör inte tider från olika datorer jämförbara.

## Bygg vidare

Förklara varför startläget inte är en ny passage av noll. Lägg till egna gränsfall och jämför de två implementationerna. Prova sedan samma idé i ett annat språk och mät skillnaden mellan kod, tester och körmiljö.

Exemplen ligger utanför `days/` så att de inte registreras som dina egna lösningar. Skriv din egen dagslösning där. Om du återanvänder kod, ange det tydligt och använd rätt spår.
