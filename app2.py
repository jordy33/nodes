from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

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
    return render_template('node_editor2.html')

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

# Save workflow endpoint
@app.route('/save_workflow', methods=['POST'])
def save_workflow():
    try:
        workflow_data = request.get_json()
        # Here you could save the workflow to a database or file
        return jsonify({
            'success': True,
            'message': 'Workflow saved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# Load workflow endpoint
@app.route('/load_workflow', methods=['GET'])
def load_workflow():
    try:
        # Here you could load a workflow from a database or file
        workflow_data = {}  # Replace with actual workflow data
        return jsonify({
            'success': True,
            'workflow': workflow_data
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
