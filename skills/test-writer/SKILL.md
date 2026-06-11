---
name: test-writer
description: Write comprehensive Unit and Integration tests for newly implemented code to ensure high coverage before moving to code review. Trigger on /test-writer and proactively whenever a new function, module, API endpoint, or feature is implemented — or whenever the user says "write tests for this", "add test coverage", "I need tests before PR", "is this well-tested?", or "cover this with tests". Do NOT move to Phase 3 (Code Review) until tests pass.
---

# Test Writer Skill (Coverage Before Review)

No code moves to code review without tests. Writing tests after the fact produces shallow, happy-path-only suites. Write tests immediately after implementation while the intended behavior is fresh, before moving to the scrutinize or post-mortem phase.

---

## Core Invariants

1. **Tests Before Review:** The AI must NOT declare an implementation "done" or suggest moving to `/scrutinize` until the test suite is written and passes.
2. **Cover the Contract, Not the Implementation:** Test observable inputs and outputs, not internal implementation details. Tests must survive a refactoring of the internals.
3. **Three Test Categories Minimum:** Every feature must have tests covering: (a) the happy path, (b) at least one edge case or boundary, (c) at least one error/failure path.
4. **No Mocking Internals You Own:** Only mock external dependencies (network calls, third-party APIs, file system). Never mock functions from the same module under test — that produces false coverage.
5. **Docs In-Sync:** After writing tests, confirm the tested behavior matches `docs/backend/endpoints.md` or `docs/system/architecture.md`.

---

## When NOT to Use
- Do NOT use this skill to write tests for code that has not yet been implemented — write tests after the feature exists (not TDD, unless the user explicitly requests it).
- Do NOT use `/test-writer` on files with no exported functions or observable public API surface.

---

## Test Templates

### Unit Test — Jest / Vitest
```js
// tests/unit/userService.test.js
import { describe, it, expect, vi } from 'vitest'
import { createUser } from '../../src/services/user.service.js'
import { db } from '../../src/db.js'

vi.mock('../../src/db.js')   // mock ONLY external dependency

describe('userService.createUser', () => {
  it('creates and returns a new user on valid input', async () => {
    db.query.mockResolvedValueOnce([{ insertId: 42 }])
    const result = await createUser({ email: 'a@b.com' })
    expect(result).toEqual({ id: 42 })
  })

  it('throws DUPLICATE_ENTRY when email already exists', async () => {
    db.query.mockRejectedValueOnce({ code: 'ER_DUP_ENTRY' })
    await expect(createUser({ email: 'a@b.com' })).rejects.toMatchObject({
      code: 'DUPLICATE_ENTRY',
    })
  })

  it('throws on empty email', async () => {
    await expect(createUser({ email: '' })).rejects.toThrow()
  })
})
```

### Integration Test — Supertest / Hoppscotch
```js
// tests/integration/users.api.test.js
import request from 'supertest'
import { app } from '../../src/app.js'

describe('POST /users', () => {
  it('returns 201 and user id on valid payload', async () => {
    const res = await request(app).post('/users').send({ email: 'new@test.com' })
    expect(res.status).toBe(201)
    expect(res.body).toHaveProperty('id')
  })

  it('returns 409 on duplicate email', async () => {
    await request(app).post('/users').send({ email: 'dup@test.com' })
    const res = await request(app).post('/users').send({ email: 'dup@test.com' })
    expect(res.status).toBe(409)
    expect(res.body.code).toBe('DUPLICATE_ENTRY')
  })

  it('returns 400 on missing email field', async () => {
    const res = await request(app).post('/users').send({})
    expect(res.status).toBe(400)
  })
})
```

---

## Workflow Steps

### Step 1: Identify the Surface Under Test
- List every exported function, API endpoint, or class method in the target file.
- For each, identify: expected inputs, expected outputs, known edge cases, and known failure modes.

### Step 2: Write Unit Tests First
- One `describe` block per function.
- Cover: happy path → edge case → error/failure. In that order.
- Run after each test block: `npm test -- --testPathPattern=<file>`.

### Step 3: Write Integration Tests
- For API endpoints, use `supertest` or equivalent to hit the running server.
- Test the full request → validation → service → response chain.
- Cover: valid request → invalid input → conflicting state.

### Step 4: Check Coverage Report
```bash
npm test -- --coverage
# Target: ≥80% line coverage on the new file(s)
# Report any uncovered branches to the user and explain why they are acceptable to skip (if applicable)
```

### Step 5: Commit Tests
```bash
git add tests/
git commit -m "test: add unit and integration tests for [feature]"
```

### Step 6: Gate on Passing
- If any test fails: stop. Fix the implementation or the test (explain which and why), then re-run.
- Only after `npm test` exits with code 0: report ready for `/scrutinize`.
