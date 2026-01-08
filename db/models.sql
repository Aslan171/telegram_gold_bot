-- users
CREATE TABLE IF NOT EXISTS users (
  user_id BIGINT PRIMARY KEY,
  username TEXT,
  display_name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  gt_balance NUMERIC(20,4) DEFAULT 0,
  g_balance NUMERIC(20,4) DEFAULT 0,
  total_spent NUMERIC(20,2) DEFAULT 0,
  public_id BIGSERIAL
);

-- deposits
CREATE TABLE IF NOT EXISTS deposits (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(user_id),
  amount_tenge NUMERIC(20,2),
  amount_gt NUMERIC(20,4),
  status TEXT DEFAULT 'pending',
  receipt_file_id TEXT,
  admin_note TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- withdrawals
CREATE TABLE IF NOT EXISTS withdrawals (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(user_id),
  amount_g NUMERIC(20,4),
  price_listing NUMERIC(20,4),
  status TEXT DEFAULT 'pending',
  screenshot_file_id TEXT,
  admin_note TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- admin notifications
CREATE TABLE IF NOT EXISTS admin_notifications (
  id BIGSERIAL PRIMARY KEY,
  type TEXT,
  entity_id BIGINT,
  user_id BIGINT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  read_by_admin BOOLEAN DEFAULT FALSE
);

