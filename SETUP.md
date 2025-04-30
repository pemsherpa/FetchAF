# FetchAF Setup Guide

This guide will walk you through setting up FetchAF (a natural language to SQL query generator) on your local machine, step by step, with no prior experience required.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Testing Your Setup](#testing-your-setup)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Prerequisites

You'll need to install the following software:

### 1. Install Docker Desktop

Docker allows you to run the application without installing all dependencies directly on your computer.

**For Windows:**

1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow the instructions
3. You may need to enable virtualization in your BIOS settings if prompted
4. After installation, start Docker Desktop from your Start menu

**For Mac:**

1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Drag the Docker icon to your Applications folder
3. Open Docker from your Applications folder
4. When prompted, provide your system password

**For Linux:**

1. Follow the official Docker installation guide for your distribution: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
2. Set up Docker to run without sudo (optional but recommended):
   ```bash
   sudo groupadd docker
   sudo usermod -aG docker $USER
   # Log out and log back in for changes to take effect
   ```

### 2. Verify Docker Installation

Open a terminal/command prompt and run:

```bash
docker --version
docker-compose --version
```

You should see version information for both commands.

### 3. Get a Cohere API Key (if you don't have one already)

1. Go to [https://dashboard.cohere.com/signup](https://dashboard.cohere.com/signup)
2. Create an account and verify your email
3. Navigate to API Keys section
4. Create a new API key and copy it (you'll need this later)

## Installation

### 1. Get the Project Files

**Option A: Clone from Git (if you're familiar with Git):**

```bash
git clone https://github.com/yourusername/FetchAF.git
cd FetchAF
```

**Option B: Download ZIP file (if you're not familiar with Git):**

1. Download the ZIP file from the shared link or email
2. Extract the ZIP file to a location on your computer
3. Open Terminal/Command Prompt
4. Navigate to the extracted folder:

   ```bash
   # On Windows
   cd C:\path\to\extracted\FetchAF

   # On Mac/Linux
   cd /path/to/extracted/FetchAF
   ```

### 2. Make Setup Scripts Executable (Mac/Linux only)

If you're on Mac or Linux, you need to make the helper scripts executable:

```bash
chmod +x manage.sh db_tools.sh
```

## Configuration

### 1. Set Up Environment Variables

Create a file named `.env` in the project folder with the following information:

```
DB_USER=postgres
DB_PASSWORD=delusional  # You can change this if you want
DB_HOST=db              # Keep this as "db" for Docker setup
DB_PORT=5432           # Standard PostgreSQL port
DB_NAME=AgileDB
COHERE_API_KEY=your_cohere_api_key_here
```

Replace `your_cohere_api_key_here` with the API key you obtained earlier.

**Windows users:** Create this file using Notepad. Save as type "All Files" and name it `.env` (including the dot at the beginning).

## Running the Application

### 1. Build and Start the Docker Containers

**On Mac/Linux:**

```bash
./manage.sh build
./manage.sh start
```

**On Windows:**

```bash
docker-compose build
docker-compose up -d
```

This process may take a few minutes the first time as it downloads all necessary components.

### 2. Check if Containers are Running

**On Mac/Linux:**

```bash
./manage.sh status
```

**On Windows:**

```bash
docker-compose ps
```

You should see two containers running: `fetchaf-app` and `fetchaf-postgres`.

### 3. Access the Application

Open your web browser and go to:

```
http://localhost:8501
```

You should now see the FetchAF interface.

## Testing Your Setup

### 1. Importing Sample Data

The application needs data to work with. We'll import some sample F1 driver data.

1. Download the sample data file from the shared location or create a file named `seed_data.sql` with the following content:

```sql
-- Create a table for F1 drivers
CREATE TABLE IF NOT EXISTS f1drivers_dataset (
    "DriverID" SERIAL PRIMARY KEY,
    "Driver" VARCHAR(100) NOT NULL,
    "Nationality" VARCHAR(50),
    "Team" VARCHAR(100),
    "Points" INT,
    "Wins" INT,
    "PodiumFinishes" INT,
    "Age" INT
);

-- Insert sample data
INSERT INTO f1drivers_dataset ("Driver", "Nationality", "Team", "Points", "Wins", "PodiumFinishes", "Age")
VALUES
('Max Verstappen', 'Netherlands', 'Red Bull Racing', 410, 19, 28, 26),
('Lewis Hamilton', 'United Kingdom', 'Mercedes', 352, 7, 12, 39),
('Charles Leclerc', 'Monaco', 'Ferrari', 280, 4, 9, 26),
('Lando Norris', 'United Kingdom', 'McLaren', 245, 2, 10, 24),
('Carlos Sainz', 'Spain', 'Ferrari', 236, 2, 6, 29),
('Oscar Piastri', 'Australia', 'McLaren', 200, 1, 5, 23),
('George Russell', 'United Kingdom', 'Mercedes', 198, 1, 2, 26),
('Sergio Perez', 'Mexico', 'Red Bull Racing', 152, 0, 2, 34),
('Fernando Alonso', 'Spain', 'Aston Martin', 140, 0, 4, 43),
('Lance Stroll', 'Canada', 'Aston Martin', 24, 0, 0, 25);
```

2. Import the sample data:

**On Mac/Linux:**

```bash
cat seed_data.sql | docker exec -i fetchaf-postgres psql -U postgres -d AgileDB
```

**On Windows:**

```bash
type seed_data.sql | docker exec -i fetchaf-postgres psql -U postgres -d AgileDB
```

### 2. Test the Application

In the FetchAF interface, try asking:

```
Show all drivers from Netherlands
```

You should see results showing Max Verstappen.

## Troubleshooting

### Common Issues:

#### "Cannot connect to the Docker daemon"

- Make sure Docker Desktop is running
- On Linux, make sure your user is in the docker group

#### "Error connecting to database"

- Verify your `.env` file has the correct credentials
- Make sure the db container is running: `docker ps | grep fetchaf-postgres`
- Check container logs: `docker logs fetchaf-postgres`

#### "Application is not responding"

- Check app logs: `docker logs fetchaf-app`
- Restart containers: `./manage.sh restart` (Mac/Linux) or `docker-compose restart` (Windows)

#### "The page isn't working" or browser errors

- Wait 30 seconds for the application to fully start
- Try a different browser
- Check if port 8501 is being used by another application

### How to Restart Everything

If you need a fresh start:

**On Mac/Linux:**

```bash
./manage.sh stop
docker volume rm karma-ai_postgres_data  # This will delete all database data!
./manage.sh start
```

**On Windows:**

```bash
docker-compose down
docker volume rm karma-ai_postgres_data  # This will delete all database data!
docker-compose up -d
```

## FAQ

### Q: Do I need to install PostgreSQL separately?

A: No. The Docker setup includes PostgreSQL.

### Q: How do I update my Cohere API key?

A: Edit the `.env` file and change the `COHERE_API_KEY` value, then restart the containers.

### Q: How can I back up my database?

A: On Mac/Linux: `./db_tools.sh backup`
On Windows: `docker exec -t fetchaf-postgres pg_dump -U postgres -d AgileDB > backup.sql`

### Q: How can I shut down everything when I'm done?

A: On Mac/Linux: `./manage.sh stop`
On Windows: `docker-compose down`

### Q: How do I see what's happening in the database?

A: You can check the database logs:
On Mac/Linux: `./manage.sh logs db`
On Windows: `docker-compose logs -f db`

### Q: How do I run this on my local network so others can access it?

A: Find your computer's IP address:

- Windows: Run `ipconfig` in Command Prompt
- Mac/Linux: Run `ifconfig` or `ip addr show` in Terminal

Then others can access the application at `http://YOUR_IP_ADDRESS:8501`

### Q: What if I want to modify the application?

A: Edit the files, then rebuild and restart:
On Mac/Linux: `./manage.sh restart`
On Windows: `docker-compose down && docker-compose up -d`
