# Nodes example in flask

## Overview
This app create a node editor that can be used to create workflows. 
The following tools are used:
- flask
- numpy
- mysql-connector-python
- json
- rete.js

## The UI Tools to create a node-based editor:
```
	1.	Vue.js as the frontend framework.
	2.	Rete.js as the core library for defining and managing the node editor.
	3.	Plugins:
	•	rete-vue-render-plugin: For rendering nodes with Vue.js.
	•	rete-connection-plugin: For creating connections between nodes.
	•	rete-area-plugin: For managing the workspace (zoom, pan, etc.).
```

### How to run the app
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python main.py
```
### Basic Example 1

Optionally you can run
```
python app1.py
```
Commands:
```
When you run the app1 you should be able to:

See the node editor canvas
Create nodes by right-clicking
Drag nodes around
Connect nodes together
Input values and see them update in real-time
```

### Basic Example 2
Optionally you can run
```
python app2.py
```

Main app Commands:
```
Added new node types:

Number (outputs a constant number)
Square (squares the input number)
Add (adds two numbers)
Multiply (multiplies two numbers)


Added a toolbar with:

Buttons for each node type
Clear All button
Visual feedback on hover


Added node deletion:

Press Delete key to remove selected nodes
Visual feedback when nodes are deleted


Added notification system:

Shows feedback for actions
Auto-dismissing notifications
Clean, modern design


Improved error handling:

Try-catch blocks for node creation
User-friendly error messages
Confirmation for clearing the editor


Better UI/UX:

Cleaner node design
Better socket visibility
Improved input controls
```
