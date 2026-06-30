<p align="center">
  <img src="https://shieldcn.dev/header/surface.svg?title=CSXIIP+School+Management+System&subtitle=Low-code+admin+system+%E2%80%94+dynamic+tables%2C+forms%2C+and+CRUD+from+DB+schema&logo=simple-icons:python&theme=dark" alt="CSXIIP" />
</p>

<p align="center">
  <a href="https://github.com/vishalxtyagi/CSXIIP/stargazers"><img src="https://shieldcn.dev/github/stars/vishalxtyagi/CSXIIP.svg" alt="Stars" /></a>
  <a href="https://github.com/vishalxtyagi/CSXIIP"><img src="https://shieldcn.dev/github/license/vishalxtyagi/CSXIIP.svg" alt="License" /></a>
  <img src="https://shieldcn.dev/github/last-commit/vishalxtyagi/CSXIIP.svg" alt="Last Commit" />
  <img src="https://shieldcn.dev/badge/status-finished-22c55e.svg" alt="Status: Finished" />
  <img src="https://shieldcn.dev/badge/GUI-Tkinter-3776AB.svg?logo=python" alt="Tkinter" />
  <img src="https://shieldcn.dev/badge/database-MySQL-4479A1.svg?logo=mysql" alt="MySQL" />
</p>

---

A "low-code" school management system: connect it to a MySQL database and it **dynamically generates tables, forms, and full CRUD interfaces from the schema** — no code changes needed to add new modules.

> **Showcase:** [vt-csxiip-school-management-system.pages.dev](https://vt-csxiip-school-management-system.pages.dev) · Class 12 CS project (2020–21)

## The core idea

```
MySQL DB schema → CSXIIP reads table structure
                       │
                       ▼
               Dynamically generates Tkinter form for each table
                       │
                       ▼
               Full CRUD UI — Create, Read, Update, Delete
               No code needed to add a new module
```

Point it at any schema and get a working admin panel. Originally built for a school to manage students, staff, fees, and attendance — but the architecture is data-driven.

## Running

```bash
git clone https://github.com/vishalxtyagi/CSXIIP
cd CSXIIP
pip install -r requirements.txt

# Edit functions.py — set your MySQL connection config:
# HOST, USER, PASSWORD, DATABASE

python main.py
```

## What it manages

- Students (enrollment, class, section)
- Staff records
- Fee tracking
- Attendance
- Any custom table — just add it to your DB schema

## Known limitations

- SQL queries use Python string formatting (`%s` style) — SQL injection risk on untrusted input
- Pickle-based session storage — not safe for multi-user or network environments
- Desktop-only (Tkinter) — would need a full rewrite for web/mobile

## What's next

- Rebuild as a web admin panel (FastAPI + React or Refine.dev)
- Parameterized queries everywhere
- Role-based access control

---

<p align="center">
  Built by <a href="https://vishalxtyagi.in">Vishal Tyagi</a> ·
  <a href="https://vt-csxiip-school-management-system.pages.dev">Showcase</a> ·
  <a href="https://github.com/vishalxtyagi/infra/blob/main/tech-debt.md">Tech debt tracker</a>
</p>
