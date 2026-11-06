import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import event, select
from sqlalchemy.orm import Session, selectinload

from database import engine
from models import Accommodation


queries = []


def count_select_queries(
    conn,
    cursor,
    statement,
    parameters,
    context,
    executemany,
):
    if statement.lstrip().upper().startswith("SELECT"):
        queries.append(statement)


with Session(engine) as session:
    event.listen(engine, "before_cursor_execute", count_select_queries)

    try:
        statement = (
            select(Accommodation)
            .options(selectinload(Accommodation.amenities))
            .order_by(Accommodation.id)
        )

        accommodations = list(session.scalars(statement).all())

        for accommodation in accommodations:
            print(
                accommodation.title,
                [amenity.name for amenity in accommodation.amenities],
            )

    finally:
        event.remove(engine, "before_cursor_execute", count_select_queries)


print(f"\nNumber of SELECT queries: {len(queries)}")

for number, query in enumerate(queries, start=1):
    print(f"\nRequest {number}:")
    print(query)
