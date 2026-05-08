import json
from pathlib import Path


DATA_PATH = Path(__file__).with_name("data").joinpath("creator_metrics.json")


def load_creator_metrics():
    with DATA_PATH.open() as metrics_file:
        return json.load(metrics_file)


def calculate_cpm(campaigns):
    total_spend = sum(campaign["spend_usd"] for campaign in campaigns)
    total_impressions = sum(campaign["impressions"] for campaign in campaigns)

    if total_impressions <= 0:
        return 0

    return round((total_spend / total_impressions) * 1000, 2)


def get_creator_cpm(creator_id):
    metrics = load_creator_metrics()
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
    }
