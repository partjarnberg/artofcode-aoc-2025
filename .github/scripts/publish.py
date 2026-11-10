"""Publish metadata only. GitHub's short-lived identity token proves the repository."""
import json
import os
import re
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
def solution_config(path):
    data = json.loads(path.read_text()) if path.exists() else {}
    if not isinstance(data, dict) or data.get('schema_version', 1) != 1:
        raise SystemExit(f'{path}: ogiltigt format.')
    sources = data.get('source_paths', ['src'])
    forbidden = {'..', '.', 'tests', 'node_modules', 'vendor', 'dist', 'build', 'target', '__pycache__', 'input', 'inputs'}
    if not isinstance(sources, list) or not 1 <= len(sources) <= 10 or any(
        not isinstance(p, str) or not re.fullmatch(r'[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)*', p)
        or forbidden.intersection(p.split('/')) for p in sources):
        raise SystemExit(f'{path}: source_paths ska vara mappar i dagslösningen, exempelvis ["src"].')
    parts = data.get('parts', [1, 2])
    if not isinstance(parts, list) or not 1 <= len(parts) <= 2 or any(type(p) is not int or p not in (1, 2) for p in parts):
        raise SystemExit(f'{path}: parts ska vara [1], [2] eller [1, 2].')
    return sources, parts


def has_source(root, sources):
    ignored = {'node_modules', 'vendor', '.git', 'dist', 'build', '__pycache__', 'target'}
    excluded = re.compile(r'(^README(?:\..*)?$|^\.gitkeep$|^(solution|run)\.json$|\.(png|jpe?g|gif|webp|ico|pdf|zip|gz|woff2?|mp[34]|exe|so|dylib)$)', re.I)
    for source in sources:
        folder = root / source
        if folder.is_symlink():
            raise SystemExit(f'{folder}: använd en vanlig källkodsmapp, inte en symlänk.')
        for file in folder.rglob('*'):
            if ignored.intersection(file.relative_to(root).parts) or excluded.search(file.name):
                continue
            if file.is_symlink():
                raise SystemExit(f'{file}: symlänkar kan inte analyseras.')
            if file.is_file() and file.stat().st_size:
                if file.stat().st_size > 100000:
                    raise SystemExit(f'{file}: källfiler får vara högst 100 kB.')
                # Discovery only: the server independently validates and counts lines.
                if file.read_bytes().strip():
                    return True
    return False


solutions = []
for root in sorted(Path('days').glob('*/*')):
    _, day, track = root.parts
    if not root.is_dir() or not re.fullmatch(r'(0[1-9]|1[0-9]|2[0-5])', day) or track not in ('manual', 'agent'):
        continue
    sources, parts = solution_config(root / 'solution.json')
    if not has_source(root, sources):
        continue
    prefix = str(root) + '/'
    if changed is not None and not any(item.startswith(prefix) or item.startswith(('shared/', 'agent/', '.github/')) or item == 'advent.json' for item in changed):
        continue
    solutions.append({'day': int(day), 'track': track, 'parts': parts})
print(f'Hittade {len(solutions)} dagslösningar att registrera. Språk identifieras av servern.')
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
summary = ['## Julstök med ART of Code', '', result['message'], '', f'Registrerade dagslösningar: {len(solutions)}. En lyckad publicering betyder att versionen är mottagen, inte att analysen är färdig.', '', '[Vad krävs för färdig analys?](https://aoc.artofcode.se/startrepot/#fardig-analys)', '']
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
