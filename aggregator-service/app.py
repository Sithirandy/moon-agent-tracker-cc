import os
import mysql.connector
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)

# Database connection details
DB_HOST = "moon-agent-db-new.c90ec204g7j0.ap-south-1.rds.amazonaws.com"
DB_PORT = 3306
DB_NAME = "moonagentdb"
DB_USERNAME = "admin"
DB_PASSWORD = "sIfJVbLwcPieJmyspfgI"

# Function to create DB connection
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Aggregator logic: Aggregating Sales Data and Generating Reports
def aggregate_sales_data():
    connection = create_db_connection()
    if not connection:
        print("Error connecting to database")
        return

    try:
        cursor = connection.cursor(dictionary=True)

        # Best performing sales teams (Agent with max sales)
        cursor.execute("""
            SELECT agent_code, SUM(sale_amount) AS total_sales 
            FROM sales 
            GROUP BY agent_code 
            ORDER BY total_sales DESC 
            LIMIT 5
        """)
        best_agents = cursor.fetchall()
        print(f"Best performing agents: {best_agents}")

        # Products that achieved sales targets
        cursor.execute("""
            SELECT product_id, SUM(sale_amount) AS total_sales 
            FROM sales 
            GROUP BY product_id 
            HAVING total_sales >= (
                SELECT price FROM product WHERE product_id = sales.product_id
            )
        """)
        target_achieving_products = cursor.fetchall()
        print(f"Products achieving sales targets: {target_achieving_products}")

        # Branch wise sales performance
        cursor.execute("""
            SELECT a.branch, SUM(s.sale_amount) AS total_sales 
            FROM sales s
            JOIN agent a ON s.agent_code = a.agent_code 
            GROUP BY a.branch
        """)
        branch_sales = cursor.fetchall()
        print(f"Branch-wise sales performance: {branch_sales}")

    except mysql.connector.Error as e:
        print(f"Database query error: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Setting up scheduled task using APScheduler
def setup_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the aggregate_sales_data function to run every hour
    scheduler.add_job(aggregate_sales_data, 'interval', hours=1)
    scheduler.start()

@app.route("/")
def health_check():
    return "Aggregator Service is running!", 200

if __name__ == "__main__":
    # Setup the scheduler for background job
    setup_scheduler()
    # Run the Flask app (optional for health check)
    app.run(host="0.0.0.0", port=5003, debug=True)