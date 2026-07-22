from pathlib import Path
import sys

from sqlalchemy import text

backend_root = Path(__file__).resolve().parents[2]
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from app.db.database import engine

with engine.connect() as connection:

    result = connection.execute(text("SELECT 1"))

    print(result.scalar())