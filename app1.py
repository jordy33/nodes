from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

class SquareNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0, "min": -100.0, "max": 100.0, "step": 0.1}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "square_value"
    CATEGORY = "math"

    def square_value(self, value):
        result = float(value * value)
        return (result,)

@app.route('/')
def index():
    return render_template('node_editor1.html')

@app.route('/process_node', methods=['POST'])
def process_node():
    data = request.get_json()
    node_id = data.get('node_id')
    input_value = float(data.get('value', 0))
    
    # Process the node calculation
    square_node = SquareNode()
    result = square_node.square_value(input_value)[0]
    
    return jsonify({
        'node_id': node_id,
        'result': result
    })

if __name__ == '__main__':
    app.run(debug=True)
