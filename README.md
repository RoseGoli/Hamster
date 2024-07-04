# Hamster Clicker 🐹
![Untitled](https://github.com/RoseGoli/Hamster/assets/70085500/8f673aeb-a823-43a5-bf80-f0410fcc00f2)

## Overview
Hamster is a Python-based project designed to collect hamster-coins 🎉. This guide will help you clone, set up, and run the project on your local machine.

## Prerequisites
- Python 3.x
- Git

## Installation

### Clone the Repository
First, clone the repository to your local machine using the following command:

```sh
git clone https://github.com/RoseGoli/Hamster.git
cd Hamster
```

### Create a Virtual Environment
It's recommended to create a virtual environment to manage dependencies. You can create and activate a virtual environment using the following commands:

For Unix/macOS:
```sh
python3 -m venv venv
source venv/bin/activate
```

For Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
With the virtual environment activated, install the required dependencies:

```sh
pip install -r requirements.txt
```

### Configure Environment Variables
Copy the example environment configuration file and edit it as necessary:

```sh
cp .env.example .env
```

Open the `.env` file and configure the necessary environment variables.
add the following variables with their respective values:
```
API_ID   = your_api_id
API_HASH = your_api_hash
TG_TOKEN = your_tg_token
OWNERS   = [owner1,owner2]
```
Make sure to replace your_api_id, your_api_hash, your_tg_token, and owners with the actual values.

### Run the Project
Finally, run the main script to start the project:

```sh
python main.py
```

## Contact
[@TheUser](https://t.me/TheUser)

Feel free to modify the sections like "Overview", "Contributing" and "Contact" according to your specific project details.
