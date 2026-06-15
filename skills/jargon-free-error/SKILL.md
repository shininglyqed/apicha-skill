---
name: jargon-free-error
description: Convert technical system exceptions (DB, network, crashes) into user-friendly bilingual (Thai/English) error messages with actionable steps. Trigger on /jargon-free-error and proactively whenever the user is writing error handlers, catch blocks, DB error callbacks, HTTP error responses, or says "the error message is confusing", "users don't understand the error", "what should I show when it fails", or "translate this error for end users".
---

# Jargon-Free Error Skill (User-Friendly Error Notifications)

Never leak technical jargon, database stack traces, file paths, or internal server error codes to users. These confuse non-technical operators and leak security vectors. Every error response must be translated into a clean, bilingual (Thai & English) instruction that tells the user exactly what went wrong and how they can fix it.

## Core Rules

You must enforce the following guidelines across error handlers and response models:

### 1. Mask Technical Jargon
- **Before (Violating):** `Error: ETIMEDOUT`, `SQL State: 23000 (Duplicate Entry for key 'users.email')`, `Cannot read properties of undefined (reading 'split')`.
- **After (Correct):** Transform internal errors into structured codes and localized customer-facing messages. Keep detailed logs on the server side (via a safe log tracker with UUIDs), but send only friendly outputs to the client.

### 2. Dual-Language & Actionable Context
Every error message returned to the user interface must follow a standard structured payload containing:
1. **Locational Message:** What went wrong in plain English and Thai.
2. **Actionable Step:** What the user should do next (e.g., "please check your input", "contact administration", "retry in a few minutes").

### 3. Common System Error Mapping Table
Use this translation guide when handling database or network errors:

| Technical Source / Exception | User-Friendly TH Message | User-Friendly EN Message | Action/Solution |
| :--- | :--- | :--- | :--- |
| **Duplicate Key / SQL 23000** | รหัสหรือข้อมูลนี้มีอยู่ในระบบแล้ว | This record already exists in the system. | กรุณาตรวจสอบรหัสแล้วลองใหม่อีกครั้ง / Please verify the identifier and try again. |
| **Foreign Key Constraint Fail** | ไม่สามารถลบหรือจัดการรายการนี้ได้ เนื่องจากข้อมูลถูกเชื่อมโยงอยู่กับส่วนอื่น | Cannot modify or delete this item because it is linked to other records. | กรุณาตรวจสอบข้อมูลอ้างอิงก่อนดำเนินการ / Please check associated data before proceeding. |
| **Timeout / ETIMEDOUT / Network** | การเชื่อมต่อกับระบบขัดข้องชั่วคราว | The system is temporarily unable to connect. | กรุณาตรวจสอบเครือข่ายอินเทอร์เน็ตของคุณแล้วลองใหม่อีกครั้ง / Please check your internet connection and try again. |
| **Validation Fail (Schema 400)** | รูปแบบข้อมูลบางอย่างไม่ถูกต้อง | Some input fields have invalid formats. | กรุณาตรวจสอบข้อมูลในช่องที่ไฮไลต์สีแดง / Please verify the data in the highlighted fields. |
| **Internal Server Error (500)** | เกิดข้อผิดพลาดทางเทคนิคภายในระบบ | A technical error occurred. | กรุณาลองใหม่อีกครั้งในภายหลัง หรือติดต่อทีมสนับสนุนหากปัญหายังคงอยู่ / Please try again later, or contact support if the issue persists. |

---

## Target Response Payload Structure
All API error responses must be mapped to this standard JSON format:

```json
{
  "statusCode": 409,
  "code": "DUPLICATE_ENTRY",
  "message": {
    "th": "รหัสนี้ถูกใช้งานไปแล้วในระบบ",
    "en": "This identifier is already in use."
  },
  "action": {
    "th": "กรุณาใช้รหัสใหม่ หรือตรวจสอบข้อมูลเดิม",
    "en": "Please use a different identifier or verify the existing record."
  },
  "errorId": "err-9b1deb4d-3b7d-4bad"
}
```
*Note: The `errorId` maps to the server-side log where the raw technical stack trace is securely stored for debugging.*

---

## Workflow Steps

### Step 1: Exception Audit
- Audit all `try/catch` blocks, Fastify error handlers, and database connection handlers.
- Identify where raw exceptions could bubble up to the client.

### Step 2: Implement a Global Error Handler
- Set up a centralized error handler at the outermost layer of your backend (e.g., Express `app.use(errorHandler)`, Fastify `setErrorHandler`, Django middleware, Rails `rescue_from`).
- Inside the handler, read the error type/status and map database or network exceptions to the friendly format using the mapping table above.
- Ensure raw stack traces are written to backend logs only (tagged with an `errorId` UUID), and only the structured friendly JSON is returned to the client.

### Step 3: Verify the Error Handler
- Trigger each mapped error type manually (e.g., insert a duplicate key, call a bad endpoint, kill the DB connection) and confirm the response JSON matches the target payload structure above — not the raw exception.
- Confirm raw stack traces do **not** appear in the client response body.
- Run the test suite: `npm test` — error response tests must pass before declaring done.

### Step 4: Update Docs
- Open `docs/backend/endpoints.md` and add an **Error Response** section listing every error `code` (e.g., `DUPLICATE_ENTRY`, `VALIDATION_ERROR`, `INTERNAL_ERROR`) alongside its `statusCode` and friendly message keys.
- This keeps the error contract visible to other engineers without reading the handler code.

