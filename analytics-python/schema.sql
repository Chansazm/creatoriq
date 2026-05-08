CREATE TABLE IF NOT EXISTS creators (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS campaign_metrics (
  id BIGSERIAL PRIMARY KEY,
  creator_id TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
  campaign_id TEXT NOT NULL,
  spend_usd NUMERIC(12, 2) NOT NULL CHECK (spend_usd >= 0),
  impressions BIGINT NOT NULL CHECK (impressions >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (creator_id, campaign_id)
);

CREATE INDEX IF NOT EXISTS campaign_metrics_creator_id_idx
  ON campaign_metrics (creator_id);
