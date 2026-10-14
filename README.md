# Aviation Flight Path Optimization Using AI

An end-to-end data pipeline and genetic algorithm designed to calculate the most cost-efficient flight trajectory while strictly avoiding dynamic weather hazards.

## 🚀 Project Architecture
1. **Optimization Engine (`src/genetic_path_func2.py`):** Uses an evolutionary algorithm to minimize the route distance. It incorporates vector-based collision detection to heavily penalize trajectories intersecting storm radiuses.
2. **Data Pipeline (`src/database_link.py` & `sql/PostgreSQL_code.psql`):** A Python script establishes a pipeline with a PostgreSQL server (hosted on Ubuntu) using `psycopg2`. It dynamically extracts environmental constraints, processes the optimal path, and logs the sequential waypoints back to the database.
3. **Business Intelligence:** A Power BI dashboard connected to the PostgreSQL LAN server visualizes the optimized trajectory and translates evolutionary metrics into business KPIs (e.g., Safety Detour Cost).

## 📊 Results
![Optimized Route](assets/dashboard_final.png)
*The model calculated a safety detour cost of +6.39 km to bypass the storm zone safely compared to a theoretical linear flight.*

## ⚙️ How to Run
1. Setup PostgreSQL using the schema provided in `sql/PostgreSQL_code.psql`.
2. Create a `.env` file in the root directory with your local database credentials (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`).
3. Execute the main pipeline:
   ```bash
   python src/database_link.pyS