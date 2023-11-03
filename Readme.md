Below is a guide on how to set up and run the project:

Assuming you have Python (version 3.9+ recommended) and pip installed:

1. **Create a new virtual environment**

First, navigate to the directory containing the project. Then you can create a virtual environment using the venv module that comes with python.

On MacOS/Linux:

```
python3 -m venv venv
```
On Windows:

```
python -m venv venv
```
"venv" is the name of your virtual environment. You can use any name you prefer. 

2. **Activate the virtual environment**

On MacOS/Linux:

```
source venv/bin/activate
```
On Windows:

```
venv\Scripts\activate
```
In the terminal, you should now see that the prompt contains "(venv)", which signals that the virtual environment is active. 

3. **Install the required packages**

Ensure that your terminal is in the root directory of the project (the one containing `requirements.txt`) and run:

```
pip install -r requirements.txt
```
This will install all the necessary packages required for the project in the virtual environment. 

4. **Run the server**

You can now run the main.py:
```
python main.py
```

The API should now be running! You can visit `http://localhost:8080`

5. **Deactivating the Virtual Environment**

When you're done working, you can deactivate the virtual environment and return to your normal shell by running:

```
deactivate
```

Remember to activate the virtual environment whenever you return to work on the project!