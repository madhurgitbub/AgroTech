import json
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
sb = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_ROLE_KEY'])
root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'data' / 'data.json').read_text(encoding='utf-8'))

existing = sb.table('products').select('id').limit(1).execute().data
if not existing:
    rows = []
    for p in data.get('products', []):
        rows.append({k: p.get(k) for k in ['id','name','category','price','unit','description','image','rating','reviews','available','location']})
    # Keep the provided numeric IDs where possible.
    sb.table('products').insert(rows).execute()
    print(f'Seeded {len(rows)} products.')
else:
    print('Products already exist; skipping product seed.')
