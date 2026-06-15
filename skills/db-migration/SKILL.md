---
name: db-migration
description: Generate version-controlled database migration files (using Knex.js with MySQL) whenever the schema changes. Trigger on /db-migration and proactively whenever a design doc or feature requires a new table, column, index, or constraint — or whenever the user says "add a column", "update the schema", "create a table", "change the database", or "the DB needs to store X". NEVER allow manual ALTER TABLE in production; every schema change must be a migration file committed to source control.
---

# DB Migration Skill (Version-Controlled Schema Changes)

Every database schema change — no matter how small — must be captured as a migration file committed to source control. Never instruct the user to run manual SQL statements directly against the database. A schema must be reproducible from scratch by running migrations in order.

---

## Core Invariants

1. **No Manual Alterations:** Never produce bare SQL `ALTER TABLE` or `CREATE TABLE` commands for the user to run by hand. Every change must live inside a migration file that is committed and tracked.
2. **Feature-Based Grouping (No Micro-migrations):** Can group related schema changes belonging to the same feature within a single migration file instead of splitting one column per file (e.g. creating a table along with its indexes and related columns).
3. **Optional Down Migrations:** The `down` function is optional. If rollback is not critical, you can write `// No rollback required`.
4. **Never Modify an Already-Run Migration:** If a migration has been committed and applied, create a new migration to correct it. Do not edit the original file.
5. **Docs In-Sync:** After generating a migration, update `docs/database/schema.md` to reflect the new schema state before declaring the task done.
6. **Knex is the Only Tool:** This project uses **MySQL** and **Knex.js** exclusively for database migrations. No other ORM/migration frameworks (like Prisma or Sequelize) or raw SQL scripts should be used.

---

## When NOT to Use
- Do NOT use this skill to seed test data — use a dedicated seed file instead.
- Do NOT generate a migration before the design in `docs/database/schema.md` has been approved.

---

## Migration File Template (Knex.js)

```js
// migrations/YYYYMMDDHHMMSS_add_deleted_at_to_users.js
exports.up = async (knex) => {
  await knex.schema.table('users', (table) => {
    table.timestamp('deleted_at').nullable().defaultTo(null)
    table.index('deleted_at')
  })
}

exports.down = async (knex) => {
  // No rollback required
}
```

---

## Workflow Steps

### Step 1: Read the Design Doc
- Open `docs/database/schema.md` and confirm the approved schema change.
- Do NOT infer schema from application code alone — the design doc is the source of truth.

### Step 2: Name the Migration
- Use a full timestamp prefix + descriptive name: `YYYYMMDDHHMMSS_description`.
- Examples: `20240611143022_add_deleted_at_to_users`, `20240611143501_create_audit_log_table`.

### Step 3: Generate the Migration File
- Write the `up` function first, then the `down` function if required (or write `// No rollback required`).
- Place the file in the project's migrations directory (e.g., `migrations/` or `db/migrations/`).

### Step 4: Verify Locally
```bash
# Run the migration
npx knex migrate:latest

# Confirm rollback works (if down function is implemented)
npx knex migrate:rollback
```

### Step 5: Commit & Update Docs
```bash
git add migrations/
git commit -m "db: add deleted_at to users table"
```
- Update `docs/database/schema.md` to reflect the new schema state.
