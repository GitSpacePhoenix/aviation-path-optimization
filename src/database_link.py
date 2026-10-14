import os
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from dotenv import load_dotenv
import csv
from genetic_path_func2 import genetic_path_f

load_dotenv()


def get_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    return psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME")
    )

def fetch_scenario_data(scenario_id):
    """
    Queries the database to extract fligth boundaries and storm data.
    Returns: START_POINT, END_POINT, and STORM tuple

    """

    conn = get_connection() #Extract póstgress data connection
    cursor = conn.cursor()  # Syntax ?

    # 1. Fetch fligth limits
    # Execute a query using SQL syntax with cursor.execute()

    cursor.execute( #declarate start and end point
        "SELECT start_x, start_y, end_x, end_y FROM scenarios WHERE scenario_id = %s;",
        (scenario_id,)

    )

    scen = cursor.fetchone()  # fetchone() meaning
    start_point = np.array([float(scen[0]), float(scen[1]) ])
    end_point = np.array([float(scen[2]), float(scen[3])])
    
    # 2. Fetchone storm data associated with the scenario

    cursor.execute( #declzarate storm coordiantes
        "SELECT center_x, center_y, radius FROM weather_zones WHERE scenario_id = %s;",
        (scenario_id, )
    )
    print(cursor.fetchone)
    print("Cursor report")
    storm_data = cursor.fetchone()
    storm = (float(storm_data[0]), float(storm_data[1]), float(storm_data[2]) )

    cursor.close()
    conn.close()

    return start_point, end_point, storm





#def save_optimized_trayectory(scenario_id, best_route):
def save_optimized_trayectory(scenario_id, best_route, final_cost, generations):
    """Deletes any existing old records for this scenario and inserts
        the new optimized waypoints into the database.
        """
    conn = get_connection()
    cursor = conn.cursor()

    try:

            # +++
        # 1. Update KPIs in the scenarios table 
        cursor.execute(
            """
            UPDATE scenarios
            SET last_optimized_cost = %s, generations_run = %s
            WHERE scenario_id = %s;
            """,
            (float(final_cost), int(generations), scenario_id)
            )
            # ++++





        #Clear previous records for this scenario to avoid duplicates
        cursor.execute("DELETE FROM optimized_trajectories WHERE scenario_id = %s;", (scenario_id,))

        # Insert each waypint with its sequence order

        for order_idx, waypoint in enumerate(best_route):
            cursor.execute(
                """       
                INSERT INTO optimized_trajectories(scenario_id, sequence_order, pos_x, pos_y)
                VALUES (%s, %s, %s, %s); 
                """, # optimzed_trajectories
                (scenario_id, order_idx, float(waypoint[0]), float(waypoint[1]))
                #    Qsuites do not comment code here
            )

        # Comit the trtansaction to save changes permanently
        conn.commit()
        print(f"Succes: Optimized trajectory for {scenario_id} saved to DB")


    except Exception as e:
        conn.rollback()
        print(f"Database error during insert: {e}")
    finally:
        cursor.close()
        conn.close()


def export_to_csv(scenario_id, route, filename="optimized_route.csv"):
    """
    Exports the waypoints to CSV file for temporary Power BI testing
    """
    try:
        with open(filename, mode ='w', newline='') as file:
            writer = csv.writer(file)
    
            #Write the header
            writer.writerow(['scenario_id', 'sequence_order', 'pos_x', 'pos_y'])

            #Write the data row by row
            for order_idx, waypoint in enumerate(route):
                writer.writerow([scenario_id, order_idx, waypoint[0], waypoint[1]])
    
        print(f"Data exported succesfully to {filename}")
    except Exception as e:
        print(f"Error Writting to CSV: {e}")







# --- Main execution  ---
if __name__ == "__main__":
    SCENARIO_ID = 1

    print("Fetching scenario from database...")
    # Dunamically load the constants from PostgreSQL!
    START_POINT, END_POINT,STORM = fetch_scenario_data(SCENARIO_ID)

    from genetic_path_func2 import genetic_path_f

    #START_POINT = np.array([0, 0])
    #END_POINT = np.array([100, 100])
    
    # Define a "storm" as a circle: (x, y, radius)
    #STORM = (50, 50, 15)

    best_final_route, final_best_cost, GENERATIONS = genetic_path_f(START_POINT, END_POINT, STORM)



    #Once the loop finishes and you extract 'best_final_route':
    print("Optimization finished, Writting results to PostgreSQL")
    save_optimized_trayectory(SCENARIO_ID, best_final_route, final_best_cost, GENERATIONS)

    # Exported CSV
    print("4. Exporting data CSV for PowerBI testing...")
    export_to_csv(SCENARIO_ID, best_final_route)

    print("Done, Pipeline complete.")




