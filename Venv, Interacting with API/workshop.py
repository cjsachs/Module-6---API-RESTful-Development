# Introduction to Virtual Environments

# What is a Virtual Environment? An isolated environment for Python projects.
# Why use Virtual Environments?
'''
    - Avoid dependency conflicts.
    - Allows different projects to use different versions of libraries.
    - Keeps the global Python environment clean.
'''

# 1. Creating & Activating a virtual environment
# Creating: "python3 -m venv venv"
# Activating: Windows: .\venv\Scripts\activate        MAC: source venv/bin/activate
# NOTE: To deactivate a virtual environment, type "deactivate" in the terminal

# 2. Installing Packages in a Virtual Environment: "pip install requests"
# This installs the requests package inside the virutal environment, isolated from the global environment.
# NOTE: The "pip list" command allows you to see installed packages.

# 3. Freezing Dependencies: "pip freeze > requirements.txt"
# This will create a file to track installed packages.
# NOTE: Always add your virtual environment to a ".gitignore" file





# Interacting with an API

# What is an API? Application Programming Interface, allows different applications to communicate with each other.
# The requests package is used to send HTTP requests.

# 1. Basic structure of an API request
import requests

response = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')
print(response) # Will print a response object, also display the status code
'''
    Common Status Codes:
    - 200s: ok/successful
    - 400s: not okay/unsuccessful
    - 500s: server is down
'''
print(response.status_code)
print(response.ok)
# Convert response into JSON data if status code is 200
if (response.status_code == 200):
    data = response.json()
    print(data["name"])

# 2. Passing Parameters
pokemon = 'charizard'
response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')

if (response.ok):
    data = response.json()
    print(data["name"])

# def get_pokemon(pokemonName):
#     response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemonName}')

# 3. Handling Errors and Exceptions (try & except): Always handle exceptions that may occur during an API request
try:
    pokemon = 25
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
    
    if (response.ok):
        data = response.json()
        print(data["name"], data["abilities"][0]["ability"]["name"])
    else:
        print('Response Unsuccessful')
except:
    print('Encountered a python error.')