# FLEETRA
<div align="center">

# 🚛 FLEETRA

### Smart Fleet. Smarter Moves.

**An intelligent transport operations platform built to simplify fleet management, automate dispatch workflows, and transform operational data into actionable insights.**

<br/>

![Odoo](https://img.shields.io/badge/Odoo-19-714B67?style=for-the-badge&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-LGPL--3-success?style=for-the-badge)
![Hackathon](https://img.shields.io/badge/Odoo-Hackathon%202026-FFB900?style=for-the-badge)

<br/>

> **Every vehicle. Every driver. Every trip. One intelligent command center.**

</div>

---

## 🌟 About FLEETRA

Fleet operations are often buried under spreadsheets, manual logbooks, disconnected expense records, and endless coordination.

**FLEETRA changes that.**

FLEETRA is a centralized **Smart Transport Operations Platform** designed to manage the complete lifecycle of transport operations — from vehicle registration and driver compliance to intelligent trip dispatching, maintenance, fuel tracking, expenses, and operational analytics.

Built for the **Odoo Hackathon 2026**, FLEETRA combines automated business workflows with smart fleet insights to help transport teams **move faster, operate safer, and make better decisions.**

---

## 🎯 The Problem

Traditional transport operations face several challenges:

- 📋 Manual vehicle and driver records
- ⚠️ Scheduling and dispatch conflicts
- 🚚 Underutilized fleet assets
- 🔧 Missed vehicle maintenance
- 🪪 Expired driver licenses
- ⛽ Inaccurate fuel tracking
- 💸 Fragmented expense records
- 📉 Poor operational visibility

FLEETRA brings these workflows into **one intelligent platform**.

---

## 💡 Our Solution

FLEETRA acts as a **Fleet Command Center** that automatically enforces operational rules and keeps vehicles, drivers, and trips synchronized.

```text
Vehicle Registered
        ↓
Driver Verified
        ↓
Trip Created
        ↓
Smart Validation Engine
        ↓
Trip Dispatched
        ↓
Vehicle + Driver → ON TRIP
        ↓
Trip Completed
        ↓
Vehicle + Driver → AVAILABLE
        ↓
Fuel & Expenses Updated
        ↓
Fleet Analytics Refreshed
```

---

## ✨ Key Features

### 📊 Smart Fleet Dashboard

Get a real-time operational overview with key fleet KPIs:

- Active Vehicles
- Available Vehicles
- Vehicles in Maintenance
- Active Trips
- Pending Trips
- Drivers On Duty
- Fleet Utilization

---

### 🚚 Vehicle Registry

Manage the complete lifecycle of fleet assets.

- Unique vehicle registration numbers
- Vehicle model and type tracking
- Maximum load capacity
- Odometer management
- Acquisition cost tracking
- Automatic vehicle status updates

**Vehicle Status**

`Available` · `On Trip` · `In Shop` · `Retired`

---

### 👨‍✈️ Driver & Safety Management

Maintain driver profiles while enforcing safety and compliance rules.

- Driver license tracking
- License category management
- License expiry monitoring
- Safety score tracking
- Driver availability status
- Automatic assignment restrictions

Drivers with an **expired license** or **suspended status** are automatically blocked from trip assignment.

---

### 🗺️ Intelligent Trip Dispatcher

Create and manage trips with automatic operational validation.

FLEETRA validates:

- Vehicle availability
- Driver availability
- Driver license validity
- Vehicle maintenance status
- Vehicle load capacity
- Existing trip assignments

**Trip Lifecycle**

`Draft` → `Dispatched` → `Completed` / `Cancelled`

---

### 🧠 Smart Dispatch Recommendation Engine

FLEETRA intelligently recommends the best **vehicle and driver combination** for a trip.

Recommendations consider:

- 🚚 Vehicle capacity fit
- ⛽ Fuel efficiency
- 👨‍✈️ Driver safety score
- 🔧 Vehicle maintenance health
- 🟢 Fleet availability

The system generates a **Smart Match Score** to help dispatchers make faster operational decisions.

> Right vehicle. Right driver. Right trip.

---

### 🔄 Automatic Status Engine

FLEETRA keeps fleet resources synchronized automatically.

| Action | Vehicle Status | Driver Status |
|---|---|---|
| Trip Dispatched | On Trip | On Trip |
| Trip Completed | Available | Available |
| Trip Cancelled | Available | Available |
| Maintenance Started | In Shop | — |
| Maintenance Closed | Available | — |

No manual status juggling. No scheduling conflicts.

---

### 🔧 Maintenance Management

Track vehicle maintenance and automatically protect dispatch operations.

When maintenance starts:

```text
Vehicle → IN SHOP
        ↓
Removed from Dispatch Pool
```

When maintenance closes:

```text
Vehicle → AVAILABLE
```

Retired vehicles remain permanently unavailable for dispatch.

---

### ⛽ Fuel & Expense Management

Centralize operational expenses across the fleet.

Track:

- Fuel consumption
- Fuel cost
- Maintenance expenses
- Toll expenses
- Parking expenses
- Other operational costs

FLEETRA automatically calculates the **total operational cost per vehicle**.

---

### 📈 Reports & Analytics

Turn transport data into actionable fleet insights.

FLEETRA calculates:

- ⛽ Fuel Efficiency
- 🚛 Fleet Utilization
- 💸 Operational Cost
- 📊 Vehicle ROI

#### Fuel Efficiency

```text
Distance Travelled / Fuel Consumed
```

#### Vehicle ROI

```text
Revenue - (Maintenance Cost + Fuel Cost)
────────────────────────────────────────
             Acquisition Cost
```

---

### 🔐 Role-Based Access Control

FLEETRA provides secure role-based access for different operational teams.

| Role | Primary Responsibility |
|---|---|
| Fleet Manager | Vehicles and maintenance |
| Dispatcher | Trips and dispatch operations |
| Safety Officer | Driver compliance and safety |
| Financial Analyst | Expenses and analytics |

Users only access the operations relevant to their role.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Odoo** | Application framework |
| **Python** | Business logic |
| **Odoo ORM** | Data management |
| **PostgreSQL** | Database |
| **XML** | Views and interface definitions |
| **JavaScript** | Interactive functionality |
| **SCSS** | Interface styling |

---

## 📁 Project Structure

```text
FLEETRA/
│
├── models/
│   ├── vehicle.py
│   ├── driver.py
│   ├── trip.py
│   ├── maintenance.py
│   ├── fuel_log.py
│   └── expense.py
│
├── views/
│   ├── vehicle_views.xml
│   ├── driver_views.xml
│   ├── trip_views.xml
│   ├── maintenance_views.xml
│   ├── fuel_views.xml
│   ├── expense_views.xml
│   └── menu_views.xml
│
├── security/
│   ├── security.xml
│   └── ir.model.access.csv
│
├── data/
│   └── demo_data.xml
│
├── static/
│   └── src/
│       ├── js/
│       ├── xml/
│       └── scss/
│
├── __init__.py
├── __manifest__.py
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/shrutirai29/FLEETRA.git
```

### 2. Navigate to the project

```bash
cd FLEETRA
```

### 3. Add FLEETRA to your Odoo addons path

```text
--addons-path=/path/to/odoo/addons,/path/to/FLEETRA
```

### 4. Update the Odoo application list

Open Odoo and navigate to:

```text
Apps → Update Apps List
```

### 5. Search for FLEETRA

```text
FLEETRA
```

Install the module and start managing your fleet. 🚛

---

## 🎬 Demo Workflow

```text
1. Register Van-05 with a maximum capacity of 500 KG
2. Register a driver with a valid driving license
3. Create a trip with 450 KG cargo
4. FLEETRA validates vehicle capacity
5. Smart Dispatch recommends the best vehicle and driver
6. Dispatch the trip
7. Vehicle and driver automatically become "On Trip"
8. Complete the trip and record fuel consumption
9. Vehicle and driver automatically become "Available"
10. Start vehicle maintenance
11. Vehicle automatically becomes "In Shop"
12. Fleet analytics and operational costs update
```

---

## 🔮 Future Scope

- 📍 Real-time GPS fleet tracking
- 🤖 Predictive vehicle maintenance
- 🌦️ Weather-aware route planning
- 🚦 Traffic-aware dispatch optimization
- 📱 Driver mobile application
- 🔔 Automated compliance alerts
- 🌱 Fleet carbon emission analytics

---

## 🏆 Built For

<div align="center">

### Odoo Hackathon 2026

**Problem Statement:** TransitOps — Smart Transport Operations Platform

**Hackathon Duration:** 8 Hours

</div>

---

## 👩‍💻 Developer

<div align="center">

### Shruti Rai

**B.Tech Computer Science Engineering — Cybersecurity**

Built with ☕, Python, Odoo and an unreasonable amount of hackathon energy. 🚛💨

</div>

---

<div align="center">

## 🚛 FLEETRA

### Smart Fleet. Smarter Moves.

**We move operations forward.**

⭐ Star the repository if you like FLEETRA!

</div>