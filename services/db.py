async def get_user_by_tg_id(tg_id):
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
        user = await cursor.fetchone()
        return dict(user) if user else None

async def add_user(tg_id, username, reg_date):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT INTO users (tg_id, username, reg_date) VALUES (?, ?, ?)",
            (tg_id, username, reg_date)
        )
        await db.commit()

async def update_user_balance(tg_id, balance=None, game_balance=None, total_paid=None):
    async with aiosqlite.connect(DATABASE) as db:
        if balance is not None:
            await db.execute("UPDATE users SET balance=? WHERE tg_id=?", (balance, tg_id))
        if game_balance is not None:
            await db.execute("UPDATE users SET game_balance=? WHERE tg_id=?", (game_balance, tg_id))
        if total_paid is not None:
            await db.execute("UPDATE users SET total_paid=? WHERE tg_id=?", (total_paid, tg_id))
        await db.commit()

# ===================== Платежи =====================
async def add_payment(user_id, amount, screenshot=None):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT INTO payments (user_id, amount, screenshot) VALUES (?, ?, ?)",
            (user_id, amount, screenshot)
        )
        await db.commit()

async def get_all_payments(status=None):
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        if status:
            cursor = await db.execute("SELECT * FROM payments WHERE status=?", (status,))
        else:
            cursor = await db.execute("SELECT * FROM payments")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def mark_payment_done(payment_id):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("UPDATE payments SET status='done' WHERE id=?", (payment_id,))
        await db.commit()


