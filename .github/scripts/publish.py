"""Publish metadata only. GitHub's short-lived identity token proves the repository."""
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = 'ART-of-Code-Advent-Publisher/1.0 (+https://aoc.artofcode.se)'

manifest = json.loads(Path('advent.json').read_text())
if not str(manifest.get('aoc_user_id', '')).isdigit():
    print('Fyll i ditt AoC-ID och år i advent.json och pusha igen. Inget har skickats.')
    raise SystemExit(0)
endpoint = os.environ['ADVENT_API_URL']
if urllib.parse.urlsplit(endpoint).scheme != 'https':
    raise SystemExit('API-adressen måste använda HTTPS.')
event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
before = event.get('before', '')
changed = None
if os.environ.get('GITHUB_EVENT_NAME') == 'push' and before and set(before) != {'0'}:
    result = subprocess.run(['git', 'diff', '--name-only', before, os.environ['GITHUB_SHA']], text=True, capture_output=True)
    if result.returncode == 0:
        changed = result.stdout.splitlines()
solutions = []
for path in sorted(Path('days').glob('*/*/solution.json')):
    _, day, track, _ = path.parts
    if not day.isdigit() or track not in ('manual', 'agent'):
        continue
    data = json.loads(path.read_text())
    if data.get('language') in (None, '', 'choose-your-language'):
        continue
    prefix = str(path.parent) + '/'
    if changed is not None and not any(item.startswith(prefix) or item.startswith(('shared/', 'agent/', '.github/')) or item == 'advent.json' for item in changed):
        continue
    solutions.append({'day': int(day), 'track': track, 'parts': data.get('parts', [1, 2])})
identity_url = os.environ['ACTIONS_ID_TOKEN_REQUEST_URL'] + '&audience=' + urllib.parse.quote(endpoint, safe='')
identity_request = urllib.request.Request(identity_url, headers={'Authorization': 'Bearer ' + os.environ['ACTIONS_ID_TOKEN_REQUEST_TOKEN'], 'User-Agent': USER_AGENT, 'Accept': 'application/json'})
with urllib.request.urlopen(identity_request, timeout=20) as response:
    token = json.load(response)['value']
print('::add-mask::' + token)
body = json.dumps({'solutions': solutions}).encode()
for attempt in range(3):
    request = urllib.request.Request(endpoint, body, {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json', 'User-Agent': USER_AGENT, 'Accept': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.load(response)
        break
    except urllib.error.HTTPError as exc:
        try:
            retry = int(exc.headers.get('Retry-After', '30'))
        except ValueError:
            retry = 30
        if exc.code in (429, 502, 503) and attempt < 2 and 0 <= retry <= 90:
            time.sleep(max(15, retry))
            continue
        print('API:t kunde inte registrera pushen. HTTP', exc.code)
        error_body = exc.read(8192)
        try:
            print(json.loads(error_body).get('error', {}).get('message', 'Försök igen senare.'))
        except (ValueError, UnicodeError):
            if exc.code == 403 and b'error code: 1010' in error_body:
                print('Cloudflare blockerade klienten före API:t (1010). Uppdatera publish.py från startrepot så att det skickar vårt User-Agent-namn.')
            else:
                print('Svaret kom inte i API:ts JSON-format. Kontakta ART of Code med länken till körningen.')
        raise SystemExit(1)
summary = ['## Julstök med ART of Code', '', result['message'], '']
if result.get('status') == 'awaiting_aoc_membership':
    summary += ['### Det här händer nu', '',
                'Vi har registrerat ditt GitHub-konto och repo. Din presentation syns nu på förstasidan (upp till en minuts cache).',
                'Vid nästa schemalagda hämtning från AoC letar vi efter ditt AoC-ID i gruppens lista för valt år.',
                'Det tar normalt upp till 15 minuter. Därefter syns du på topplistorna.', '',
                'Om du inte dyker upp: kontrollera AoC-ID och år i advent.json och att du gått med i gruppen på AoC.',
                'Rätta vid behov och pusha igen. Du behöver inte ändra ditt AoC-visningsnamn.', '']
summary += ['[Öppna årets topplistor](' + result['leaderboard_url'] + ')', '',
            'Nya commits sparas som nya versioner. Samma commit skapar inte dubbletter.']
with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as output:
    output.write('\n'.join(summary) + '\n')
print(result['message'])
