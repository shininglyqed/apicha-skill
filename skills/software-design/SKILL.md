---
name: software-design
description: Design software architectures and produce modular design proposals under `docs/` before any code is written. Trigger this skill on /software-design and proactively whenever the user says "I want to build", "we need a system for", "design a feature", "how should I structure this", "plan out the architecture", "I have a new requirement", or introduces scope that touches more than one service or module — even if they don't say the word "design". In medium-to-large projects, treat the `docs/` folder as the sole source of truth to prevent redundant codebase-wide scans.
---

# Software Design Skill (Strict Design-First & Modular Documentation)

Always adopt a strict "Design-First" stance. Do NOT modify implementation code, create source code files, or run installation commands until the design proposal has been drafted/updated across modular `.md` files in the `docs/` folder, and explicitly approved by the user.

**Token Optimization & Anti-Scanning Invariant:**
To prevent wasting tokens on scanning large directories repeatedly:
- The markdown files under `docs/` serve as the canonical **Source of Truth** for the project's architecture, routes, database schemas, and components.
- Do NOT run project-wide grep searches or file scans on every task. Instead, read the specific design file (e.g. `docs/backend/endpoints.md`) first to identify exactly which files need to be modified.
- Update the design documentation *first* whenever requirements evolve.

## Fixed Tech Stack & Constraints

You must strictly design the system around the following pre-approved technologies:
- **Backend API:** Fastify (Node.js REST API framework)
- **Real-time / WebSocket:** `ws` package OR `uWebSockets.js` (choose based on performance needs, but limit to these two)
- **Database:** MySQL (Relational Database only)
- **Front-end:** Must ask and clarify whether the user wants **Vanilla JavaScript** or **React** before finalizing the design.

---

## Workflow Steps

You must follow these steps in order. Do not jump to writing application code.

### Step 1: Ingestion & Clarify Front-end Stack
Analyze the user's requirements and immediately ask clarifying questions to align on design parameters:
1. **Clarify Frontend:** Ask whether the user prefers **Vanilla JavaScript** or **React**.
2. **System Boundaries & Constraints:** What external systems must this integrate with? What are the limitations or restrictions?
3. **Data & Traffic Volume:** What is the scale? (e.g., requests per second, storage size, concurrent users).

### Step 2: Create or Update Modular Design Documents
Write or update the design files under the `docs/` directory, structured by components to prevent reading large, monolithic design documents:

1. **`docs/system/architecture.md` (System Topology)**
   - High-level architectural pattern (e.g. Layered Architecture, Clean Architecture adjusted for Fastify).
   - Component responsibilities (Client, Fastify REST API, WebSocket Server, MySQL DB).
   - **Both** `graph TD` (System Topology) and `sequenceDiagram` (User event/data flows) Mermaid diagrams.
2. **`docs/backend/endpoints.md` (Fastify & WebSockets Spec)**
   - API routes, method, request validation schema definitions, and response payloads.
   - WebSocket message/event names, payloads, and state cleanup rules.
   - Authentication protocols (JWT, API keys, WS Handshake auth rules).
3. **`docs/frontend/components.md` (Client-side Design)**
   - View/component hierarchy and layout mapping.
   - State management strategy (React state/context or Vanilla JS custom store) and key routes.
4. **`docs/database/schema.md` (MySQL Schema Spec)**
   - Key MySQL tables, fields, data types, indexes, and primary/foreign key relations (DDL/SQL format).
   - Database migration strategy.

### Step 3: Present for Review & Iterate
- Provide the user with direct markdown file links to the updated design documents in `docs/`.
- Highlight key changes (especially network boundaries, route schemas, and database relations).
- Incorporate feedback, update the corresponding documentation files, and repeat until approved.

### Step 4: Hand-off to Implementation
- Once approved, proceed to formulate an implementation plan or task list based on the approved design files, editing only the specific source files mapped in the design.

### Step 5: Keep Documentation In-Sync (Post-Implementation Update)
- **CRITICAL INVARIANT:** Immediately after writing, modifying, or refactoring any code files, you **MUST** update the corresponding design/architecture files under `docs/` (`docs/system/architecture.md`, `docs/backend/endpoints.md`, `docs/frontend/components.md`, or `docs/database/schema.md`) to reflect the exact implementation details.
- Never let code and design diverge. If an implementation detail changed during coding (e.g., modified route paths, additional database keys, altered component props), adjust the documentation file immediately as the final step of the task before declaring it complete.

---

## Technical Diagram Conventions

When writing Mermaid diagrams inside the markdown:
- Use double quotes `""` for node labels containing special characters, brackets, or parentheses to avoid parser syntax errors.
- Always implement **BOTH** a `graph TD` for system topology and a `sequenceDiagram` for user event/data flows.
- **Never mix multiple diagram types in a single code block.** Write them in separate, dedicated ` ```mermaid ` code blocks.
- Ensure correct sequence diagram syntax (use `participant` in singular form).

### Example Embedded Diagrams

```mermaid
graph TD
    Client["Client (React / Vanilla JS)"] -->|HTTP / REST| Fastify["Fastify Backend API"]
    Client -->|WS Protocol| WS["WebSocket Server (ws / uWebSockets.js)"]
    Fastify -->|Connection Pool| MySQL[("MySQL Database")]
    WS -->|Query / Persist| MySQL
```

```mermaid
sequenceDiagram
    actor User
    participant UI as Client (Front-end)
    participant API as Fastify Backend
    participant WS as WebSocket Server
    participant DB as MySQL DB

    User->>UI: Click "Submit/Action" Button
    UI->>API: POST /api/v1/action (Payload)
    API->>DB: INSERT INTO logs / UPDATE status
    DB-->>API: Confirm Save
    API-->>UI: Response 200 OK (Success)
    
    Note over UI,WS: If real-time update is needed
    API->>WS: Trigger Broadcast Event
    WS-->>UI: WS Message: "update_broadcast"
    UI->>User: Update UI State / Show Toast Notification
```

## Target Project Structure
All designs must conform to or reference the following monorepo/directory architecture:

```text
my-app/
├── apps/
│   ├── backend/                 # Fastify API & WebSocket Server
│   │   ├── src/
│   │   │   ├── config/          # Environment variables & DB connection pool setup
│   │   │   │   ├── env.js       # Configures ENV variables (PORT, JWT_SECRET)
│   │   │   │   └── database.js  # Establishes MySQL connection pool
│   │   │   │
│   │   │   ├── plugins/         # Fastify core ecosystem extensions
│   │   │   │   ├── db.js        # Registers MySQL client as a global 'app.mysql' plugin
│   │   │   │   └── websocket.js # Initializes ws/uWebSockets.js server binding
│   │   │   │
│   │   │   ├── routes/          # Request routers split by consumer types
│   │   │   │   ├── internal/    # [Internal API] Used by our own front-end (Auth, CRUD)
│   │   │   │   ├── external/    # [External API] Third-party webhooks and public endpoints
│   │   │   │   └── websocket/   # [WS Endpoints] Connection management & real-time handlers
│   │   │   │
│   │   │   ├── services/        # Business logic & operational orchestrators
│   │   │   │   ├── user.service.js
│   │   │   │   └── integration.service.js # Coordinates outbound third-party API/WS calls
│   │   │   │
│   │   │   └── app.js           # Main application entry point registering plugins & routes
│   │   ├── package.json
│   │   └── .env
│   │
│   └── frontend/                # Client-side user interface folder
│       # (Structure will vary based on user framework choice: React vs Vanilla JS)
└── docs/                        # Project documentation repository (Source of Truth)
    ├── system/
    │   └── architecture.md      # High-level architecture & Mermaid diagrams
    ├── backend/
    │   └── endpoints.md         # API route schemas, controllers, websocket events
    ├── frontend/
    │   └── components.md        # UI component tree, routes, and state
    └── database/
        └── schema.md            # MySQL database DDL and schema details
```

## Mandatory Security Context (Zero-Trust Architecture)
Even if running inside a private company intranet, you must explicitly enforce and document the following security strategies across different entry points to ensure clear boundaries and avoid logic pollution:

1. **Internal API (`routes/internal/`): User-Centric Protection**
   - Must use **JWT (JSON Web Tokens)** or **HttpOnly Cookie Sessions** to authenticate human operators/engineers.
   - Every request must verify the user's role before accessing business services to support data auditing and log tracking ("Who changed what?").

2. **External API (`routes/external/`): Machine-to-Machine Protection**
   - Dedicated for automated third-party integrations, automated scripts, or webhooks.
   - Must strictly require an **API Key** passed in headers or a **Webhook Secret Signature Verification** (e.g., HMAC validation).
   - Must be isolated from user session logic to prevent bad automated scripts from flooding or crashing core application flows.

3. **WebSocket Endpoints (`routes/websocket/`): Pre-Flight Handshake Protection**
   - Authentication must be validated at the earliest gate: **During the HTTP Upgrade / Handshake Request**.
   - If no valid JWT token is provided, the server must **Reject the Handshake immediately (HTTP 401/403)** to save memory overhead and protect server resources from dangling unauthenticated connections.