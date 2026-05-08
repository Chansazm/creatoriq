import json
import os
from pathlib import Path

import psycopg

from analytics import normalize_database_url


DATA_PATH = Path(__file__).with_name("data").joinpath("creator_metrics.json")
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def main():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is required")

    metrics = json.loads(DATA_PATH.read_text())

    with psycopg.connect(normalize_database_url(database_url)) as connection:
        with connection.cursor() as cursor:
            cursor.execute(SCHEMA_PATH.read_text())

            for creator_id, creator in metrics.items():
                cursor.execute(
                    """
                    INSERT INTO creators (id, name)
                    VALUES (%s, %s)
                    ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
                    """,
                    (creator_id, creator["name"]),
                )

                for campaign in creator["campaigns"]:
                    cursor.execute(
                        """
                        INSERT INTO campaign_metrics (
                            creator_id,
                            campaign_id,
                            spend_usd,
                            impressions
                        )
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (creator_id, campaign_id)
                        DO UPDATE SET
                            spend_usd = EXCLUDED.spend_usd,
                            impressions = EXCLUDED.impressions
                        """,
                        (
                            creator_id,
                            campaign["campaign_id"],
                            campaign["spend_usd"],
                            campaign["impressions"],
                        ),
                    )

    print("Seeded Postgres creator metrics")


if __name__ == "__main__":
    main()
