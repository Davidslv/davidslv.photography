-- One row per page view, updated as the visitor reads (latest summary wins). No IPs, no cookies, no names.
CREATE TABLE IF NOT EXISTS views (
  pv TEXT PRIMARY KEY,          -- random id made by the page, dies with the page
  seq INTEGER NOT NULL,         -- summary number from that page view; only higher seq overwrites
  day TEXT NOT NULL,            -- YYYY-MM-DD (UTC)
  ts INTEGER NOT NULL,          -- unix seconds of first summary
  path TEXT NOT NULL,
  ref TEXT,                     -- referrer host or utm_source, e.g. instagram.com, whatsapp, google
  device TEXT,                  -- phone | tablet | desktop
  vw INTEGER,                   -- viewport width, px
  country TEXT,                 -- from Cloudflare, two letters
  scroll INTEGER,               -- deepest scroll, % of page
  ended INTEGER,                -- 1 if they reached the end
  secs INTEGER,                 -- seconds the page was visible
  last_photo TEXT,              -- last photo that was on screen
  photos TEXT,                  -- JSON {photo: seconds on screen}
  clicks TEXT                   -- JSON {target: count}
);
CREATE INDEX IF NOT EXISTS views_day ON views(day);
CREATE INDEX IF NOT EXISTS views_path ON views(path);
