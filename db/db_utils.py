import asyncpg
import os
from decimal import Decimal
from typing import Optional, Dict, Any

_pool: Optional[asyncpg.Pool] = None

# =========================
# INIT / CLOSE
# =========================

async def init_db_pool():
    """Инициализация пула БД через DATABASE_URL из env"""
    global _pool

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL не найден! Проверьте .env или Variables на сервере")

    _pool = await asyncpg.create_pool(
        dsn=database_url,
        min_size=1,
        max_size=10
    )

    await _apply_migrations()



async def close_db_pool():
    global _pool
    if _pool:
        await _pool.close()


async def _apply_migrations():
    """
    Применяет SQL из models.sql (создание таблиц)
    """
    global _pool

    sql_path = os.path.join(os.path.dirname(__file__), "models.sql")

    if not os.path.exists(sql_path):
        raise RuntimeError(f"models.sql не найден по пути {sql_path}")

    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()

    async with _pool.acquire() as conn:
        await conn.execute(sql)

# =========================
# USERS
# =========================

async def ensure_user(user_id: int, username: Optional[str] = None, display_name: Optional[str] = None):
    global _pool
    async with _pool.acquire() as conn:
        exists = await conn.fetchval("SELECT 1 FROM users WHERE user_id=$1", user_id)
        if not exists:
            await conn.execute(
                "INSERT INTO users (user_id, username, display_name) VALUES ($1, $2, $3)",
                user_id,
                username or "",
                display_name or ""
            )


async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    global _pool
    async with _pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE user_id=$1", user_id)
        return dict(row) if row else None


async def get_balances(user_id: int) -> Dict[str, Decimal]:
    user = await get_user(user_id)
    if not user:
        return {"gt_balance": Decimal("0"), "g_balance": Decimal("0")}
    return {
        "gt_balance": Decimal(user.get("gt_balance") or 0),
        "g_balance": Decimal(user.get("g_balance") or 0)
    }

# =========================
# DEPOSITS
# =========================

async def create_deposit(user_id: int, amount_tenge: Decimal, amount_gt: Decimal) -> int:
    global _pool
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO deposits (user_id, amount_tenge, amount_gt, status) VALUES ($1,$2,$3,'pending') RETURNING id",
            user_id, float(amount_tenge), float(amount_gt)
        )
        deposit_id = row["id"]
        await conn.execute(
            "INSERT INTO admin_notifications (type, entity_id, user_id) VALUES ('deposit',$1,$2)",
            deposit_id, user_id
        )
        return deposit_id


async def attach_deposit_receipt(deposit_id: int, file_id: str):
    global _pool
    async with _pool.acquire() as conn:
        await conn.execute("UPDATE deposits SET receipt_file_id=$1 WHERE id=$2", file_id, deposit_id)


async def approve_deposit(deposit_id: int, admin_id: int) -> bool:
    global _pool
    async with _pool.acquire() as conn:
        dep = await conn.fetchrow("SELECT * FROM deposits WHERE id=$1 AND status='pending'", deposit_id)
        if not dep:
            return False
        await conn.execute("UPDATE deposits SET status='approved' WHERE id=$1", deposit_id)
        await conn.execute(
            "UPDATE users SET gt_balance = gt_balance + $1, total_spent = total_spent + $2 WHERE user_id=$3",
            float(dep["amount_gt"]), float(dep["amount_tenge"]), dep["user_id"]
        )
        await conn.execute(
            "INSERT INTO admin_notifications (type, entity_id, user_id) VALUES ('deposit_approved',$1,$2)",
            deposit_id, dep["user_id"]
        )
        return True


async def reject_deposit(deposit_id: int, admin_id: int, reason: Optional[str] = None):
    global _pool
    note = f"Rejected by {admin_id}: {reason or ''}"
    async with _pool.acquire() as conn:
        await conn.execute(
            "UPDATE deposits SET status='rejected', admin_note = COALESCE(admin_note,'') || $1 WHERE id=$2",
            note, deposit_id
        )
        await conn.execute("INSERT INTO admin_notifications (type, entity_id) VALUES ('deposit_rejected',$1)", deposit_id)
        return True

# =========================
# WITHDRAWALS
# =========================

async def create_withdrawal(user_id: int, amount_g: Decimal, price_listing: Decimal) -> int:
    global _pool
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO withdrawals (user_id, amount_g, price_listing, status) VALUES ($1,$2,$3,'pending') RETURNING id",
            user_id, float(amount_g), float(price_listing)
        )
        withdrawal_id = row["id"]
        await conn.execute(
            "INSERT INTO admin_notifications (type, entity_id, user_id) VALUES ('withdrawal',$1,$2)",
            withdrawal_id, user_id
        )
        return withdrawal_id


async def attach_withdraw_screenshot(withdraw_id: int, file_id: str):
    global _pool
    async with _pool.acquire() as conn:
        await conn.execute("UPDATE withdrawals SET screenshot_file_id=$1 WHERE id=$2", file_id, withdraw_id)


async def approve_withdrawal(withdraw_id: int, admin_id: int) -> bool:
    global _pool
    async with _pool.acquire() as conn:
        w = await conn.fetchrow("SELECT * FROM withdrawals WHERE id=$1 AND status='pending'", withdraw_id)
        if not w:
            return False
        balance = await conn.fetchval("SELECT g_balance FROM users WHERE user_id=$1", w["user_id"])
        if balance is None or balance < w["amount_g"]:
            return False
        await conn.execute("UPDATE withdrawals SET status='approved' WHERE id=$1", withdraw_id)
        await conn.execute("UPDATE users SET g_balance = g_balance - $1 WHERE user_id=$2", float(w["amount_g"]), w["user_id"])
        await conn.execute(
            "INSERT INTO admin_notifications (type, entity_id, user_id) VALUES ('withdrawal_approved',$1,$2)",
            withdraw_id, w["user_id"]
        )
        return True


async def reject_withdrawal(withdraw_id: int, admin_id: int, reason: Optional[str] = None):
    global _pool
    note = f"Rejected by {admin_id}: {reason or ''}"
    async with _pool.acquire() as conn:
        await conn.execute(
            "UPDATE withdrawals SET status='rejected', admin_note = COALESCE(admin_note,'') || $1 WHERE id=$2",
            note, withdraw_id
        )
        await conn.execute(
            "INSERT INTO admin_notifications (type, entity_id) VALUES ('withdrawal_rejected',$1)",
            withdraw_id
        )
        return True

# =========================
# ADMIN
# =========================

async def get_pending_notifications():
    global _pool
    async with _pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM admin_notifications WHERE read_by_admin = FALSE ORDER BY created_at ASC"
        )
        return [dict(r) for r in rows]


async def mark_notification_read(notification_id: int):
    global _pool
    async with _pool.acquire() as conn:
        await conn.execute("UPDATE admin_notifications SET read_by_admin = TRUE WHERE id=$1", notification_id)



