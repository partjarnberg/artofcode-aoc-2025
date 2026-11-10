# Agentarbetet

Dag 1 skapades tillsammans med Codex i en interaktiv session. Se [arbetsinstruktionen](instructions/day01.md) och [lösningens README](../days/01/agent/README.md) för kod, tester och Dockerkommandon.

Det finns ännu inget fristående automatiserat agentramverk att installera. Du kan ge arbetsinstruktionen till ditt eget kodverktyg och fortsätta utvecklingen. Pär valde uppgift och gav agenten indata; svaren lämnades genom hans redan inloggade AoC-session. `.private/` och eventuella lokala nycklar får aldrig följa med i Git.

Nästa övning är att bygga en adapter under `src/` som hämtar en uppgift, anropar vald modell, testar lösningen och samlar verifierbar modellmetadata. Låt deltagaren styra när svar får lämnas. Dagens Dockerfile kör bara lösningsprogrammet och startar ingen modell.
