# Process × Role × Skill Intelligence Graph

> An Enterprise AI intelligence platform that connects business processes, activities, roles, skills, and AI opportunities into a structured intelligence graph.

## Overview

Enterprise AI transformation is not simply about asking an LLM questions.

Organizations need to understand:

- Which business activities exist inside a process
- Which roles perform those activities
- Which skills those roles require
- Where AI can augment or automate work
- Which roles and skills are affected by AI
- How AI-generated insights can become persistent enterprise knowledge

This project addresses that problem by building an interconnected **Process × Role × Skill Intelligence Graph** with an AI-assisted process analysis layer.

---

# Architecture

```text
                         ┌─────────────────────┐
                         │      Next.js UI      │
                         │                     │
                         │ Processes           │
                         │ Roles               │
                         │ Skills              │
                         │ AI Opportunities    │
                         │ Impact Explorer     │
                         │ Search              │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │       REST API      │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
          ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
          │ Intelligence │  │ AI Service   │  │   Evidence   │
          │ Graph APIs   │  │              │  │    Layer     │
          └──────────────┘  └──────┬───────┘  └──────────────┘
                                   │
                                   ▼
                           ┌──────────────┐
                           │ AI Provider  │
                           │ Abstraction  │
                           └──────┬───────┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                         ▼                 ▼
                  ┌────────────┐   ┌────────────┐
                  │MockProvider│   │ Future LLM │
                  │            │   │ Providers  │
                  └────────────┘   └────────────┘
                         │
                         ▼
                  ┌──────────────────┐
                  │ Graph Persistence│
                  │     Service      │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │   PostgreSQL     │
                  │ Intelligence DB  │
                  └──────────────────┘
```

---

# Intelligence Graph

The core domain model connects enterprise entities:

```text
Industry
   │
   ▼
Value Chain Stage
   │
   ▼
Process
   │
   ▼
Activity
   ├──────────────► Role
   │                  │
   │                  ▼
   │                Skill
   │
   └──────────────► AI Opportunity
                         │
                         ├── Impacted Roles
                         └── Impacted Skills
```

This allows the system to answer questions such as:

- What roles participate in this process?
- What skills are required?
- Where can AI intervene?
- Which roles and skills are affected?
- How does AI change a particular activity?

---

# Core Features

## 1. Process Intelligence

Users can browse enterprise business processes and their activities.

Example:

```text
Assortment Planning
│
├── Define Product Assortment
├── Evaluate Product Demand
├── Analyze Category Performance
├── Approve Assortment
└── Review Seasonal Assortment
```

Each activity can be explored independently.

---

## 2. AI-Assisted Process Analysis

A user can select an existing process and choose:

**Analyze with AI**

The AI provider generates structured:

- Activities
- Roles
- Skills
- AI Opportunities

The important design decision is that the result is **not treated as disposable text**.

Instead:

```text
Process
   │
   ▼
AI Analysis
   │
   ▼
Structured Analysis
   │
   ├── Activities
   ├── Roles
   ├── Skills
   └── AI Opportunities
          │
          ▼
   Graph Persistence
          │
          ▼
   PostgreSQL
```

AI-generated knowledge becomes part of the enterprise intelligence graph.

---

# 3. Pluggable AI Provider Architecture

The application uses an AI provider abstraction:

```text
Process Analysis API
        │
        ▼
    AI Service
        │
        ▼
    AIProvider
        │
        ├── MockProvider
        │
        └── Future Production Provider
```

The API layer does not depend directly on a particular AI implementation.

This allows a production LLM provider to be introduced without redesigning the API or graph persistence layer.

### Current Provider

The project includes a deterministic `MockProvider`.

It provides:

- Reproducible results
- Offline execution
- Deterministic tests
- No external API dependency

The architecture is designed so that this can later be replaced by a production AI provider.

---

# 4. Graph Persistence

The `GraphPersistenceService` converts AI-generated analysis into graph entities.

It performs get-or-create operations for:

- Activities
- Roles
- Skills
- AI Opportunities

It also creates the relationships between them.

For example:

```text
AI-Assisted Category Analytics
           │
           ├── Merchandising Analyst
           │
           ├── Category Analytics
           ├── Demand Analysis
           └── Sales Analysis
```

The persistence operation is transaction-scoped and committed only after successful processing.

---

# 5. Idempotent Persistence

Repeated AI analysis does not continuously create duplicate graph entities.

Entity matching uses normalized names to identify existing:

- Activities
- Roles
- Skills
- AI Opportunities

This makes the ingestion process safe to repeat.

The test suite explicitly verifies this behavior.

---

# 6. Impact Explorer

The Impact Explorer explains how AI affects a specific business activity.

For example:

```text
Analyze Category Performance
            │
            ├── AI Opportunity
            │      └── AI-Assisted Category Analytics
            │
            ├── Impacted Role
            │      └── Merchandising Analyst
            │
            └── Impacted Skills
                   ├── Category Analytics
                   ├── Demand Analysis
                   ├── Sales Analysis
                   └── Data Analysis
```

The interface exposes:

- Impact type
- Automation level
- AI pattern
- Impacted roles
- Impacted skills
- Role transformation
- Skill transformation
- Future state
- Evidence

---

# 7. Evidence Layer

The platform supports evidence associated with intelligence graph entities.

Evidence contains:

- Source title
- Source type
- Snippet
- Source URL
- Retrieval timestamp
- Metadata

This provides a foundation for explainable enterprise intelligence.

---

# 8. Global Search

Users can search across the intelligence graph.

Supported entities include:

- Activities
- Processes
- Roles
- Skills
- AI Opportunities

Example:

```text
Search: Merchandising Analyst

        ↓

Role
Merchandising Analyst
```

---

# Technology Stack

## Backend

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Alembic
- Pydantic
- Pytest

## Frontend

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

## Infrastructure

- Docker
- Docker Compose
- PostgreSQL

---

# Project Structure

```text
assignment-11/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── db/
│   │   └── main.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── graph_persistence.py
│   │   └── providers/
│   │       ├── base.py
│   │       └── mock.py
│   │
│   ├── alembic/
│   └── tests/
│
├── frontend/
│   ├── app/
│   │   ├── processes/
│   │   ├── roles/
│   │   ├── skills/
│   │   ├── ai-opportunities/
│   │   ├── impact/
│   │   └── search/
│   │
│   └── lib/
│       └── api.ts
│
├── docker-compose.yml
└── README.md
```

---

# Database Model

The PostgreSQL database contains the major intelligence entities:

```text
industries
value_chain_stages
processes
activities
roles
skills
ai_opportunities
evidence
```

Relationship tables include:

```text
process_activities
activity_roles
role_skills
activity_ai_opportunities
ai_opportunity_role_impacts
ai_opportunity_skill_impacts
```

Database schema evolution is managed using Alembic.

---

# API

## Processes

```text
GET  /api/processes
GET  /api/processes/{process_id}
POST /api/processes/{process_id}/analyze
GET  /api/processes/{process_id}/activities
```

## Activities

```text
GET /api/activities
GET /api/activities/{activity_id}
GET /api/activities/{activity_id}/roles
GET /api/activities/{activity_id}/ai-opportunities
```

## Roles

```text
GET /api/roles
GET /api/roles/{role_id}
GET /api/roles/{role_id}/skills
GET /api/roles/{role_id}/processes
```

## Skills

```text
GET /api/skills
GET /api/skills/{skill_id}
GET /api/skills/{skill_id}/roles
GET /api/skills/{skill_id}/processes
```

## AI Opportunities

```text
GET /api/ai-opportunities
GET /api/ai-opportunities/{opportunity_id}
GET /api/ai-opportunities/{opportunity_id}/roles
GET /api/ai-opportunities/{opportunity_id}/skills
```

## Intelligence

```text
GET /api/impact/activity/{activity_id}
GET /api/evidence/{entity_type}/{entity_id}
GET /api/search?q={query}
```

---

# Running the Project

## Requirements

The easiest way to run the complete system is with Docker Desktop.

### Start

From the project root:

```bash
docker compose up --build
```

### Services

| Service | Address |
|---|---|
| Frontend | http://localhost:3002 |
| Backend | http://localhost:8002 |
| PostgreSQL | localhost:5433 |

### Health Check

```text
GET http://localhost:8002/health
```

Expected:

```json
{
  "status": "ok"
}
```

---

# Running Tests

```bash
cd backend
pytest -v
```

Current result:

```text
9 passed
```

The test suite covers:

- API health
- Activity impact
- Evidence
- Global search
- Skill search
- AI opportunity retrieval
- AI process analysis
- Graph persistence
- Idempotent persistence

---

# End-to-End Workflow

The complete enterprise workflow is:

```text
1. Select Process
       ↓
2. Analyze with AI
       ↓
3. Generate Activities
       ↓
4. Generate Roles
       ↓
5. Generate Skills
       ↓
6. Generate AI Opportunities
       ↓
7. Persist into Intelligence Graph
       ↓
8. Map Impacted Roles
       ↓
9. Map Impacted Skills
       ↓
10. Explore AI Impact
```

This transforms AI output into persistent enterprise intelligence.

---

# Example

### Business Process

**Assortment Planning**

> Planning the product assortment and determining which products should be offered across retail channels.

### AI-generated Activity

**Analyze Category Performance**

### Role

**Merchandising Analyst**

### Skill

**Category Analytics**

### AI Opportunity

**AI-Assisted Category Analytics**

### Result

```text
Business Activity
       │
       ▼
AI Opportunity
       │
       ├── Role Impact
       │      └── Merchandising Analyst
       │
       └── Skill Impact
              ├── Category Analytics
              ├── Demand Analysis
              ├── Sales Analysis
              └── Data Analysis
```

The user can then open the Impact Explorer to understand how AI changes the activity and workforce requirements.

---

# Engineering Principles

### Structured AI

AI output is converted into structured enterprise entities instead of remaining an unstructured response.

### Separation of Concerns

The system separates:

- API layer
- AI service
- AI providers
- Graph persistence
- Database models
- Frontend

### Idempotency

Repeated analysis does not unnecessarily duplicate graph entities.

### Transaction Safety

Graph persistence commits only after successful processing.

### Extensibility

The AI provider abstraction allows future production AI providers without changing the core API architecture.

### Explainability

Evidence and explicit graph relationships provide context around intelligence results.

---

# Future Production Extensions

The current architecture provides a foundation for:

- Production LLM provider integration
- Retrieval-Augmented Generation
- Enterprise document ingestion
- Human approval workflows
- AI confidence scoring
- Provenance tracking
- Workforce scenario modeling
- Skill gap analysis
- Role transformation forecasting
- Authentication and RBAC
- Audit logging
- Observability
- Background AI processing
- Production deployment

---

# Demonstration Flow

For a technical demonstration:

```text
Processes
    ↓
Assortment Planning
    ↓
Analyze with AI
    ↓
Generated Activities
    ↓
Analyze Category Performance
    ↓
Explore Activity Impact
    ↓
AI-Assisted Category Analytics
    ↓
Merchandising Analyst
    ↓
Impacted Skills
```

The demonstration shows the complete journey from a business process to AI-driven workforce transformation.

---

# Project Status

## Completed

- [x] Intelligence graph domain
- [x] Process management
- [x] Activity management
- [x] Role management
- [x] Skill management
- [x] AI opportunity management
- [x] Graph relationships
- [x] Impact Explorer
- [x] Evidence layer
- [x] Global search
- [x] AI process analysis
- [x] Pluggable AI provider architecture
- [x] AI graph persistence
- [x] Idempotent persistence
- [x] REST API
- [x] Next.js frontend
- [x] Docker deployment
- [x] Automated test coverage
- [x] End-to-end workflow

---

## Enterprise AI Design Summary

The central architectural idea is:

> **AI should not only generate answers — it should generate structured enterprise knowledge that can be persisted, connected, explored, and used for downstream workforce transformation analysis.**

This project implements that principle through the Process × Role × Skill Intelligence Graph.
