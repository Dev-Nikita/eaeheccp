"""Check sealed result/source hashes and regenerated manuscript numerical text."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
release=Path(os.environ.get('HCADSE_RESULTS','results/v1.1-submission-results/data')).resolve().parent
manifest=json.loads((release/'manifest.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in manifest['data_sha256'].items():assert sha(release/'data'/n)==h,n
for n,h in manifest['source_sha256'].items():assert sha(release/'source'/n)==h,n
paths=[Path('manuscript/generated_numbers.tex'),*Path('manuscript/generated').glob('*.tex')]
before={str(p):p.read_bytes() for p in paths}
subprocess.run([sys.executable,'experiments/make_claims.py'],check=True)
assert all(Path(p).read_bytes()==v for p,v in before.items()),'Generated numerical prose changed: rebuild PDF'
print('Sealed source/data hashes and regenerated numerical prose: PASS')
