# hackweek2024-moods User Mood Detector

## Overview
The **User Mood Detector** is a tool designed to help support agents quickly assess the mood of customers based on the tickets they write. The system analyzes the text in customer support tickets, determines the mood of the customer, and displays a corresponding GIF that represents this mood to the support agents.

## Installation

### Prerequisites

- Python 3.x
- Node.js and npm

### Step 1: Clone the Repository

`git clone https://github.com/khatiwadakeren/hackweek2024-moods.git`  
`cd hackweek2024-moods`


### Step 2: Set Up the Client
`cd client`  
`npm install`

### Step 3: Set Up the Server
`cd server`  
`python3 -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

## Running the app
Start the server using `uvicorn main:app`.  
Serve the client-side application with npm (e.g., `npm start`).
