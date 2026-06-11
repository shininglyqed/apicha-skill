---
name: db-migration
description: Generate version-controlled database migration files (Knex, Sequelize, Prisma, or raw SQL) whenever the schema changes. Trigger on /db-migration and proactively whenever a design doc or feature requires a new table, column, index, or constraint — or whenever the user says "add a column", "update the schema", "create a table", "change the database", or "the DB needs to store X". NEVER allow manual ALTER TABLE in production; every schema change must be a migration file committed to source control.
---

# DB Migration Skill (Version-Controlled Schema Changes)

Every database schema change — no matter how small — must be captured as a migration file committed to source control. Never instruct the user to run manual SQL statements directly against the database. A schema must be reproducible from scratch by running migrations in order.

---

## Core Invariants

1. **No Manual Alterations:** Never produce bare SQL `ALTER TABLE` or `CREATE TABLE` commands for the user to run by hand. Every change must live inside a migration file that is committed and tracked.
2. **One Change per Migration:** Each migration file must represent a single, atomic schema change (e.g., "add `deleted_at` to `users`", not "add 5 columns to 3 tables"). This keeps rollback safe and history readable.
3. **Always Provide a Down Migration:** Every `up` migration must have a matching `down` that fully reverses it. Never leave `down` empty or as a no-op.
4. **Never Modify an Already-Run Migration:** If a migration has been committed and applied, create a new migration to correct it. Do not edit the original file.
5. **Docs In-Sync:** After generating a migration, update `docs/database/schema.md` to reflect the new schema state before declaring the task done.

---

## When NOT to Use
- Do NOT use this skill to seed test data — use a dedicated seed file instead.
- Do NOT generate a migration before the design in `docs/database/schema.md` has been approved.

---

## Migration File Templates

### Knex (JavaScript / TypeScript)
```js
// migrations/20240611_001_add_deleted_at_to_users.js
exports.up = async (knex) => {
  await knex.schema.table('users', (table) => {
    table.timestamp('deleted_at').nullable().defaultTo(null)
    table.index('deleted_at')
  })
}

exports.down = async (knex) => {
  await knex.schema.table('users', (table) => {
    table.dropIndex('deleted_at')
    table.dropColumn('deleted_at')
  })
}
```

### Prisma
```prisma
// In schema.prisma — then run: npx prisma migrate dev --name add_deleted_at_to_users
model User {
  id         Int       @id @default(autoincrement())
  email      String    @unique
  deleted_at DateTime?
}
```

### Raw SQL (framework-agnostic)
```sql
-- migrations/V2__add_deleted_at_to_users.sql  (Flyway/Liquibase naming)
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP NULL DEFAULT NULL;
CREATE INDEX idx_users_deleted_at ON users (deleted_at);

-- Rollback (store in separate down file):
-- DROP INDEX idx_users_deleted_at ON users;
-- ALTER TABLE users DROP COLUMN deleted_at;
```

---

## Workflow Steps

### Step 1: Read the Design Doc
- Open `docs/database/schema.md` and confirm the approved schema change.
- Do NOT infer schema from application code alone — the design doc is the source of truth.

### Step 2: Name the Migration
- Use a timestamp prefix + descriptive name: `YYYYMMDD_NNN_<what_changes>_<on_which_table>`.
- Examples: `20240611_001_add_deleted_at_to_users`, `20240611_002_create_audit_log_table`.

### Step 3: Generate the Migration File
- Write the `up` function first, then the `down` function immediately after.
- Place the file in the project's standard migrations directory (e.g., `migrations/`, `db/migrations/`, `prisma/migrations/`).

### Step 4: Verify Locally
```bash
# Run the migration
npx knex migrate:latest        # Knex
npx prisma migrate dev         # Prisma
npx sequelize-cli db:migrate   # Sequelize

# Confirm rollback works
npx knex migrate:rollback
npx prisma migrate reset       # Prisma (dev only)
```

### Step 5: Commit & Update Docs
```bash
git add migrations/
git commit -m "db: add deleted_at to users table"
```
- Update `docs/database/schema.md` to reflect the new schema state.
