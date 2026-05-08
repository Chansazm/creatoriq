import json
import os
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import psycopg
from psycopg.rows import dict_row


DATA_PATH = Path(__file__).with_name("data").joinpath("creator_metrics.json")
DATABASE_URL = os.getenv("DATABASE_URL")
METRICS_API_URL = os.getenv("CREATOR_METRICS_API_URL")


def normalize_database_url(database_url):
    if database_url and database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql://", 1)

    return database_url


def get_database_connection():
    return psycopg.connect(normalize_database_url(DATABASE_URL), row_factory=dict_row)


def get_creator_cpm_from_postgres(creator_id):
    if not DATABASE_URL:
        return None

    query = """
        SELECT
            c.id AS creator,
            c.name AS creator_name,
            COUNT(cm.id)::int AS campaign_count,
            COALESCE(SUM(cm.spend_usd), 0)::float AS total_spend_usd,
            COALESCE(SUM(cm.impressions), 0)::bigint AS total_impressions
        FROM creators c
        LEFT JOIN campaign_metrics cm ON cm.creator_id = c.id
        WHERE c.id = %s
        GROUP BY c.id, c.name
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (creator_id,))
            row = cursor.fetchone()

    if row is None:
        return None

    total_impressions = row["total_impressions"]
    total_spend = round(row["total_spend_usd"], 2)

    return {
        "creator": row["creator"],
        "creator_name": row["creator_name"],
        "campaign_count": row["campaign_count"],
        "total_spend_usd": total_spend,
        "total_impressions": total_impressions,
        "cpm": calculate_cpm_from_totals(total_spend, total_impressions),
        "source": "postgres",
    }


def load_local_creator_metrics():
    with DATA_PATH.open() as metrics_file:
        return json.load(metrics_file)


def load_remote_creator_metrics():
    if not METRICS_API_URL:
        return None

    try:
        with urlopen(METRICS_API_URL, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except (OSError, URLError, json.JSONDecodeError):
        return None


def load_creator_metrics():
    remote_metrics = load_remote_creator_metrics()

    if remote_metrics is not None:
        return remote_metrics, "remote_api"

    return load_local_creator_metrics(), "local_fallback"


def calculate_cpm(campaigns):
    total_spend = sum(campaign["spend_usd"] for campaign in campaigns)
    total_impressions = sum(campaign["impressions"] for campaign in campaigns)

    return calculate_cpm_from_totals(total_spend, total_impressions)


def calculate_cpm_from_totals(total_spend, total_impressions):
    if total_impressions <= 0:
        return 0

    return round((total_spend / total_impressions) * 1000, 2)


def get_creator_cpm(creator_id):
    postgres_cpm = get_creator_cpm_from_postgres(creator_id)

    if postgres_cpm is not None:
        return postgres_cpm

    if DATABASE_URL:
        return None

    metrics, source = load_creator_metrics()
    creator = metrics.get(creator_id)

    if creator is None:
        return None

    campaigns = creator["campaigns"]
    total_spend = round(sum(campaign["spend_usd"] for campaign in campaigns), 2)
    total_impressions = sum(campaign["impressions"] for campaign in campaigns)

    return {
        "creator": creator_id,
        "creator_name": creator["name"],
        "campaign_count": len(campaigns),
        "total_spend_usd": total_spend,
        "total_impressions": total_impressions,
        "cpm": calculate_cpm(campaigns),
        "source": source,
    }
