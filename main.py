from flask import Flask, render_template, request, jsonify
import numpy as np
import mysql.connector  # Import mysql.connector
from mysql.connector import Error  # Import Error for exception handling
import json

app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'gpscontrol',
    'password': 'qazwsxedc',
    'database': 'nodes'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Modified save workflow endpoint
@app.route('/save_workflow', methods=['POST'])
def save_workflow():
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500

    try:
        workflow_data = request.get_json()
        name = workflow_data.get('name')
        data = json.dumps(workflow_data.get('data'))

        cursor = connection.cursor()
        query = "INSERT INTO workflows (name, data) VALUES (%s, %s)"
        cursor.execute(query, (name, data))
        connection.commit()

        return jsonify({
            'success': True,
            'id': cursor.lastrowid,
            'message': 'Workflow saved successfully'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Modified load workflow endpoint
@app.route('/load_workflow/<int:workflow_id>', methods=['GET'])
def load_workflow(workflow_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT data FROM workflows WHERE id = %s", (workflow_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'success': False, 'error': 'Workflow not found'}), 404

        return jsonify({
            'success': True,
            'data': json.loads(result['data'])
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Add workflow list endpoint
@app.route('/list_workflows', methods=['GET'])
def list_workflows():
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, created_at, updated_at FROM workflows")
        workflows = cursor.fetchall()
        return jsonify({'success': True, 'workflows': workflows})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Node operation handlers
class NodeOperations:
    @staticmethod
    def number(value):
        return float(value)
    
    @staticmethod
    def square(value):
        return float(value * value)
    
    @staticmethod
    def add(a, b):
        return float(a + b)
    
    @staticmethod
    def multiply(a, b):
        return float(a * b)

# Main route to render the node editor
@app.route('/')
def index():
    return render_template('node_editor.html')

# API endpoint to process node operations
@app.route('/process_node', methods=['POST'])
def process_node():
    try:
        data = request.get_json()
        node_type = data.get('type')
        inputs = data.get('inputs', {})
        
        result = None
        
        if node_type == 'number':
            result = NodeOperations.number(inputs.get('value', 0))
        elif node_type == 'square':
            result = NodeOperations.square(inputs.get('value', 0))
        elif node_type == 'add':
            result = NodeOperations.add(
                inputs.get('num1', 0),
                inputs.get('num2', 0)
            )
        elif node_type == 'multiply':
            result = NodeOperations.multiply(
                inputs.get('num1', 0),
                inputs.get('num2', 0)
            )
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# Error handler for 404
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

# Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
