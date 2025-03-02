# Local Ollama RAG Chat

CHATBOT is an AI-driven conversational assistant designed for seamless interaction. Built with Python and Poetry, it leverages a modular architecture, configurable settings, and Docker support for deployment. The project is structured to facilitate extensibility and maintainability.

---

## 📂 Project Structure
```
CHATBOT/
│── .github/                 # GitHub workflows and CI/CD configurations
│── data/                    # Dataset and storage files
│── docs/                    # Project documentation (MkDocs source)
│── documents/               # Reference materials and reports
│── src/                     # Source code
│   ├── utils/               # Utility functions and helpers
│── .env.example             # Example environment variables file
│── .gitignore               # Git ignore rules
│── config.yml               # Configuration settings
│── docker-compose.yml       # Docker Compose configuration
│── Dockerfile               # Docker container setup
│── install_ollama.bat       # Windows installation script for Ollama
│── install_ollama.ps1       # PowerShell installation script for Ollama
│── install_docker.ps1       # PowerShell installation script for Docker
│── LICENSE                  # License file
│── mkdocs.yml               # MkDocs documentation configuration file
│── pyproject.toml           # Poetry project and dependency management file
│── README.md                # Project documentation (this file)
│── RUN.bat                  # Windows batch script to execute the chatbot
│── run.py                   # Main application entry point
```

---

## 🛠 Prerequisites
Before proceeding with installation, ensure the following dependencies are installed:

- **Python** (>=3.10,<3.13)
- **Poetry** (for dependency management)
- **Docker & Docker Compose** (optional, for containerized deployment)
- **MkDocs** (for building and serving documentation)

To install Poetry, run:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verify the installation:
```bash
poetry --version
```

To install MkDocs, use pip:
```bash
pip install mkdocs
```

---

## 🚀 Installation

### Install Dependencies
Poetry automatically creates and manages a virtual environment:
```bash
poetry install
```

To activate the Poetry-managed virtual environment:
```bash
poetry shell
```

---

## ⚙️ Configuration

### Environment Variables
Copy the `.env.example` file and configure it according to your setup:
```bash
cp .env.example .env
```
Modify `.env` as needed.

### Application Configuration
Modify `config.yml` to adjust chatbot settings.

---

## ▶️ Running the Application

### Run Using Poetry
To start the chatbot:
```bash
poetry run python run.py
```

Alternatively, use the provided batch script:
```bash
./RUN.bat
```

---

## 🐳 Docker Installation

Before deploying the application with Docker, ensure that both Docker and Docker Compose are installed on your system. Follow the instructions below for your operating system:

1. **Download Docker Desktop:**  
   Visit [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) and download the installer.

2. **Install Docker Desktop:**  
   Run the installer and follow the on-screen instructions. If prompted, enable WSL 2 integration.

3. **Verify Installation:**  
   Open Command Prompt or PowerShell and run:
   ```bash
   docker --version
   docker-compose --version
   ```
   You should see the installed versions of Docker and Docker Compose.

---

## 🐳 Docker Deployment

### Build the Docker Image
```bash
docker-compose build
```

### Start the Chatbot Container
```bash
docker-compose up -d
```
To stop the container:
```bash
docker-compose down
```

---

## 📚 Documentation

This project includes comprehensive documentation built with **MkDocs**. The documentation source files are located in the `docs/` directory and are configured using the `mkdocs.yml` file.

### Serve Documentation Locally
To preview the documentation during development, run:
```bash
mkdocs serve
```
This will start a local server (typically at [http://127.0.0.1:8000](http://127.0.0.1:8000)) where you can view the documentation.

### Build the Static Site
To generate the static documentation site for deployment, run:
```bash
mkdocs build
```
The output will be placed in the `site/` directory, which you can then deploy to your preferred hosting platform (e.g., GitHub Pages).

