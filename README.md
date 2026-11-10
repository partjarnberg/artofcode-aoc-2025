# Julstök med ART of Code

Skapa ett eget publikt repo med **Use this template → Create a new repository**. Mallen har workflow, båda spåren och instruktioner klara. Du behöver ingen inloggning på vår sajt och ingen API-nyckel till oss.

**Alla deltagare visas på sajten.** När din första push har registrerats visas ditt namn, din presentation och repolänk på förstasidan. Du behöver ingen färdig lösning. Att bara gå med i AoC-listan registrerar dig inte här.

## Kom igång

1. Gå med i ART of Codes privata lista på [Advent of Code 2025](https://adventofcode.com/2025/leaderboard/private) med koden `1487429-4647410c`.
2. Fyll i `aoc_user_id`, `display_name` och `year` i `advent.json`. Logga in på AoC och öppna [Settings](https://adventofcode.com/2025/settings). Vid namnalternativet **Anonymous User #123456** står ditt numeriska ID efter `#`. Du behöver inte välja alternativet eller ändra namn. Skriv numret i `aoc_user_id`; `display_name` är namnet du själv vill visa hos oss. Använd 2025 för övning och 2026 för premiären, med ett separat repo per år. Förstasidan samlar dina årsrepon i samma presentation, med årsmärken och ett filter för anmälningsår.
   Skriv gärna en kort presentation i `bio` (högst 160 tecken), till exempel vem du är och vad du vill prova. Fältet är valfritt och kan ändras med en ny push.
3. Committa `advent.json` och pusha till repots default branch, vanligtvis `main`. Workflowet registrerar ditt GitHub-konto och repo automatiskt. Öppna **Actions → Publicera Advent-lösningar → senaste körningen** för besked om att registreringen tagits emot. Vi kontrollerar ditt AoC-ID i gruppens lista vid nästa synk, normalt inom 15 minuter. Därefter syns du på topplistorna. Du behöver inte ändra ditt AoC-visningsnamn.
4. Skriv lösning, egna tester, Dockerfile och README under `days/01/manual/` eller `days/01/agent/`. Lägg själva koden i `src/`; du behöver ingen extra config-fil.
5. Lämna svaret på AoC och pusha koden. Workflowet registrerar versionen; servern väntar på godkännande för rätt år, dag och del innan den analyserar.
6. Fortsätt förbättra och pusha. Historiken sparar nya commits; samma commit ger inga dubbletter. Workflowet kan också startas manuellt via **Run workflow**.

För testmiljön kan en repository variable `ADVENT_API_URL` peka på test-API:ts `/api/v1/github/push`. Standard är produktion på `https://aoc.artofcode.se/api/v1/github/push`. GitHub Actions behöver `contents: read` och `id-token: write`, vilket redan är angivet i workflowet. Token skapas kortvarigt av GitHub; du ska inte skapa en egen nyckel.

Vi litar på att du anger ditt eget AoC-ID. GitHub bekräftar repo och ägare; AoC-listan bekräftar medlemskap, inte kontoägarskap. Om AoC-resultaten inte visas, kontrollera ID, år och gruppmedlemskap. Rätta filen och pusha igen. Kontakta ART of Code om ett redan anslutet ID är fel.

[Förstå startrepot, fil för fil](https://aoc.artofcode.se/startrepot/) visar vad varje fil gör och hur pushflödet fungerar.

## När är analysen färdig?

1. **Du är registrerad.** `advent.json` innehåller rätt år och ditt numeriska AoC-ID. Repot är publikt på ditt personliga GitHub-konto och ID:t finns i vår AoC-grupp för samma år.
2. **Koden är pushad till `main`** (eller repots default branch). Lägg lösningen i `days/NN/manual/src/` eller `days/NN/agent/src/`, där `NN` är två siffror, exempelvis `01`. Minst en källfil måste innehålla text. Tomma mappar och undervisningsexemplen registreras inte.
3. **Publiceringen har lyckats.** Öppna **Actions → Publicera Advent-lösningar → senaste körningen**. Sammanfattningen visar hur många dagslösningar som registrerades. En grön körning betyder att API:t har tagit emot versionen; analysen kan fortfarande vänta.
4. **Rätt år, dag och del är godkända på AoC.** Vi hämtar resultat högst en gång per kvart. Del 1 kan analyseras även om del 2 återstår. AoC godkänner ditt svar, inte en viss GitHub-commit.
5. **Workern har läst och analyserat koden.** Efter AoC-synken tar kön normalt ytterligare någon minut, längre om många väntar. Om GitHubs API-kvot är slut väntar vi tills GitHub tillåter nya anrop och fortsätter automatiskt; du behöver inte pusha igen. När resultatet finns under **Topplistor → Kodrader**, med rätt år, dag, del och spår samt länk till den analyserade versionen, är analysen färdig.

**Ingen `solution.json` behövs för standardstrukturen.** Språket identifieras automatiskt. Båda delarna registreras som standard och väntar var för sig på AoC-godkännande. Om programmet bara stöder en del kan du begränsa det med den valfria konfigurationen nedan.

Lägg egna tester i `tests/`, och dokumentera körning och huvudidé i README. Skriv en Dockerfile så att andra kan prova lösningen. De är en del av vår övning i att dela körbar, begriplig kod, men dagens statiska analys kräver eller kör inte Docker eller testerna. En modellrapport är valfri och behövs endast för att dina AI-modeller ska kunna räknas.

Analysen läser högst 40 textfiler, 100 kB per fil och 1 MB totalt. Koden ska vara UTF-8. Beroenden, byggartefakter, README, rapporter och kända binärfiler räknas inte. Inputfiler, privata kataloger, hemligheter, loggar och symlänkar ska inte finnas i analysområdet; upptäckta sådana filer stoppar analysen. En tom eller felaktig analys blir inte ett resultat med noll kodrader.

### Bara om du behöver en annan struktur

Skapa `solution.json` i dagslösningens mapp **endast om du behöver ändra standardvalen**. Exempel för kod i `code/`, bara del 1 och egen delad kod:

```json
{
  "source_paths": ["code"],
  "parts": [1],
  "shared_paths": ["shared/manual"]
}
```

Alla fält är valfria. Utan filen används `source_paths: ["src"]`, `parts: [1, 2]` och `shared_paths: []`. Källkodsmapparna anges relativt dagens spårmapp, exempelvis `days/01/manual/`. Delade filer eller mappar anges från repots rot och måste ligga under `shared/`. Ange bara egen kod som lösningen faktiskt använder; den räknas med i kodraderna. Sökvägar får inte lämna dagsmappen med `../`. Tester ligger separat under `tests/`. Du ska inte ange programmeringsspråk.

Äldre filer med `schema_version: 1` och `language` fungerar fortfarande, men språkfältet används inte. Ta bort filen om du använder standardvalen. Vid ändring av en dagslösning, dess konfiguration eller gemensam kod registrerar nästa push en ny version för analys.

## Hitta i repot

```text
agent/                    Ditt eget agentsystem och dess instruktioner
days/01/manual/           Din egen dagslösning
days/01/agent/            Agentens producerade dagslösning
shared/                   Din återanvändbara kod
days/01/agent/run.json     Valfri rapport över verktyg och modeller
runs/                     Dokumentation av rapportformatet
examples/2025/day01/      Två färdiga undervisningsexempel (spoilers)
.private/                 Dina privata indata och lokala loggar; aldrig Git
.github/workflows/        Pushflödet till ART of Codes API
```

Färdiga exempel ligger utanför `days/` och registreras inte som dina egna lösningar. Båda skapades med AI-stöd för undervisning. Hantverksexemplet visar arbetssättet; det är inte en deltagares handskrivna tävlingsinlämning.

## Körkontrakt för dina lösningar

Dockerfile beskriver hur språk, beroenden och kod sätts ihop till en körmiljö. Det gör att andra kan klona ditt repo och prova lösningen med Docker, utan att installera ditt språk lokalt. Att själv beskriva miljön, testa den och dokumentera körningen är en del av övningen.

Bygg från repots rot med en Dockerfile per dag och spår:

```sh
docker build -f days/01/manual/Dockerfile -t advent-day01 .
docker run --rm -i advent-day01 --part 1 < .private/inputs/01.txt
```

Programmet läser stdin, skriver svaret på stdout och diagnostik på stderr. Dina privata indata skickas in först vid körning; de ska inte byggas in i imagen. `.dockerignore` utesluter `.private/` från byggkontexten. Publicera egna små testdata som andra kan använda utan tillgång till dina AoC-indata.

Dag-1-exemplens Dockerfiles kör tester under bygget. Startrepots workflow **Verify teaching examples** bygger dessutom båda exempelcontainrarna och kontrollerar CLI:t för båda delarna med egna testdata. Detta workflow gäller exemplen; lägg till motsvarande kontroll för dina egna `days/`-lösningar om du vill ha den i CI.

Vår server gör i dagsläget statisk analys och kör inte deltagarkod eller Dockerfiles. Dockerfile räknas som infrastruktur, separat från lösningens kodrader. Vi mäter eller rangordnar ingen exekveringstid. Docker ger ett gemensamt sätt att starta programmen, men en rättvis prestandajämförelse skulle även behöva samma testdata, hårdvara, resursgränser och upprepade mätningar.

I agentspåret kör dagens container den producerade lösningen. Själva agentsystemet och instruktionerna för att köra det hör hemma i `agent/`; att köra dagslösningen startar inte en AI-modell.

## Gör det lätt att lära av dig

Beskriv installation och versioner, körkommandon, tester, kodens huvudidé och ett förbättringsförslag. För agenten: dela instruktioner, verktyg/modeller, hur den startas och hur man ändrar flödet. Länka till inspiration. Topplistorna länkar till ditt repo så att andra kan förstå, prova och bygga vidare.

## Modeller och topplistor

Låt agenten skriva en valfri `run.json` i agentens dagsmapp, exempelvis `days/01/agent/run.json`. Se [rapportformatet](runs/README.md). Rapportera faktiskt modell-ID från anropets svar, inte bara verktygsnamnet. Modeller märks alltid som självrapporterade. Samma modell räknas en gång per år; nya versioner och språk finns kvar i historiken.

Kodrader jämförs per dag, del och spår. Inlämningstid ger inga poäng.

## Öppet och privat

- Publicera egen kod, tester med egna data, Dockerfiles och agentinstruktioner.
- Publicera aldrig AoC:s uppgiftstext, personliga inputfiler, sessionscookies, modellnycklar eller råa agentloggar.
- `.gitignore` och `.dockerignore` hjälper men tar inte bort filer som redan checkats in.
- Deltagandet är publikt: namn, valfri presentation och repolänk visas efter första registrerade pushen. AoC-medlemskap öppnar för stjärnor och analyser.
- Redovisa modeller och mänskliga ingripanden ärligt. Okända mätvärden ska inte gissas.

[Onboarding och spelregler](https://aoc.artofcode.se/kom-igang/) · [Stöd Eric Wastl och Advent of Code](https://adventofcode.com/2026/support)
