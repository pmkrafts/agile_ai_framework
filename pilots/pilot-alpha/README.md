# Pilot Project Alpha: Internal Task Management API

**Project ID:** pilot-alpha  
**Type:** Internal tool  
**Risk Level:** Low  
**Sprint Duration:** 1 week

---

## 1. Business Problem

Internal teams need a simple API to create, assign, and track tasks. Current process uses spreadsheets and email, causing delays and missed assignments.

## 2. Success Metrics

- API supports CRUD operations for tasks
- Authentication required for all operations
- 80%+ test coverage
- Deployed to staging within 1 week

## 3. Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- Docker
- pytest

## 4. User Stories

### US-001: User Authentication

**As a** team member, **I want** to log in with email and password, **so that** I can access my tasks.

```gherkin
Scenario: Successful login
  Given a registered user with email "user@example.com" and password "SecurePass123"
  When the user submits the login form
  Then the response status code should be 200
  And the response should contain a valid JWT token

Scenario: Failed login
  Given a registered user with email "user@example.com" and password "WrongPass"
  When the user submits the login form
  Then the response status code should be 401
```

### US-002: Create Task

**As a** team member, **I want** to create a task, **so that** I can track my work.

```gherkin
Scenario: Create task with valid data
  Given an authenticated user
  When they POST to /tasks with title and description
  Then the response status code should be 201
  And the task should be stored in the database

Scenario: Create task without title
  Given an authenticated user
  When they POST to /tasks without a title
  Then the response status code should be 400
```

### US-003: List Tasks

**As a** team member, **I want** to list my tasks, **so that** I can prioritize my work.

```gherkin
Scenario: List tasks
  Given an authenticated user with existing tasks
  When they GET /tasks
  Then the response status code should be 200
  And the response should contain their tasks
```

## 5. Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   FastAPI   │────▶│  PostgreSQL │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 6. Acceptance Criteria

- All Gherkin scenarios pass
- Code coverage ≥80%
- Security scan clean
- CTO approves architecture
- CEO accepts demo

## 7. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Auth library integration issues | Medium | Use well-known library (python-jose) |
| Database migration complexity | Low | Use SQLAlchemy Alembic |

---

**Approved by:**

- [ ] CEO
- [ ] CTO
