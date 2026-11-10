# Mitt agentsystem

Fyll i instruktionerna så att någon annan kan köra och vidareutveckla agenten från en ny klon.

## Installera och konfigurera

- Ange verktyg, versioner, modeller och nödvändiga lokala beroenden.
- Beskriv miljövariabler med tomma eller ofarliga exempelvärden. Dela aldrig nycklar eller sessioner.
- Ange hur år, dag och del väljs. Året ska matcha `advent.json`; 2025 är vår övningssäsong.

## Kör och testa

Lägg in dina faktiska kommandon för installation, en agentkörning och tester. Beskriv hur man provar flödet med egna små testdata och utan att skicka svar till AoC. Förklara vilka steg som kräver mänsklig hjälp.

## Förstå och ändra flödet

- Beskriv hämta → lösa → testa → lämna svar → publicera och var respektive steg finns i koden.
- Lägg agentinstruktioner i `instructions/` och länka till dem här.
- Visa hur man ändrar en instruktion, byter modell och återupptar en avbruten körning.
- Beskriv ett förbättringsförslag och vad du har lärt dig av tidigare försök.

## Data och rapporter

Spara dagens lösning i `days/01/agent/`. Cachelagra AoC-material i `.private/`, respektera väntetider och stoppa återkommande fel. Kör inte loopar som gissar svar.

Publicera bara en sammanfattning av körningen i `runs/`, utan uppgiftstext, indata eller konversationer. Referera till exakt lösningscommit och den commit som agentsystemet kördes från.
