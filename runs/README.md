# Rapportera modellförsök

Lägg en valfri `run.json` i `days/01/agent/`, bredvid dagslösningens README. Vid nästa push läses den från samma exakta commit som lösningen. Den analyseras först när AoC har godkänt den aktuella delen. Gamla analyserade rapporter ligger kvar i årets historik.

```json
{
  "schema_version": 1,
  "source": "participant_report",
  "tool": { "name": "my-agent", "version": null },
  "human_interventions": null,
  "models": []
}
```

`models` innehåller ett objekt per unikt par av `provider` och `model_id`, högst 20. Varje objekt har:

| Fält | Betydelse |
| --- | --- |
| `provider` | Leverantörens identifierare, exempelvis `openai` eller `anthropic`. |
| `model_id` | Exakt modell-ID från API-svar eller verktygets rapport. Gissa inte utifrån verktygsnamnet. |
| `requests` | Antal anrop, eller `null` om okänt. |
| `input_tokens` | Rapporterade indatatoken, eller `null`. |
| `output_tokens` | Rapporterade utdatatoken, eller `null`. |

Skriv bara modeller som faktiskt användes för den här lösningen. Gör listan kumulativ över dess försök om du vill redovisa flera provade modeller. Verktyg som Codex, Claude Code eller Pi är inte modell-ID:n. En tom lista betyder okänd eller ej rapporterad modellanvändning, inte att ingen modell användes.

Låt helst adaptern runt modell-API:t fylla i rapporten automatiskt från svarens metadata. Flera anrop till samma modell samlas i samma post. Exportera endast metadata; aldrig promptar, svar, AoC-text/indata, nycklar, cookies eller råa agentloggar. Fälten är valfria enligt tabellen, men okända tal ska vara `null`, inte noll.

Alla rapporter märks **självrapporterade**. GitHub-signaturen bekräftar vilket repo och vilken commit som rapporterade, inte att modellen verkligen körts. Topplistan räknar distinkta leverantör/modell-ID-par per deltagare och år bland AoC-godkända, analyserade agentlösningar. Modellalias kan överlappa. Verktygsnamn och tokenantal ger inga extra poäng.

En ny push analyserar en ändrad rapport. Samma commit ger inga nya modeller eller extra poäng. Filer i denna `runs/`-katalog är dokumentation; bara `run.json` i dagslösningen läses av analysen.
