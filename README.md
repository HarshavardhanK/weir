# Weir: Multi-Agent LLM Travel Query and Recommendation App

Welcome to Weir, a multi-agent LLM-powered application designed to provide personalized travel recommendations. Weir processes natural language queries to help you find the best flights, hotels, and destinations within your budget. This interactive chat-based system leverages GPT-4o Mini (or any compatible LLM) to enhance your travel planning experience.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Interactive Chat Interface**: Engage with Weir through a chat-based interface powered by GPT-4o Mini or any compatible LLM.
- **Multi-Agent System**: Utilizes multiple agents to handle different aspects of travel planning, including flights, hotels, and destinations.
- **Budget-Friendly Recommendations**: Provides travel plans that fit within the user's specified budget.
- **Natural Language Processing**: Understands and processes user queries in natural language for a seamless experience.
- **Scalable and Extensible**: Built with scalability in mind, allowing for easy integration of additional features and services.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.11](https://www.python.org/downloads/)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/weir.git
   cd weir
   ```

2. **Set Up Environment Variables**:

   Create a `.env` file in the root directory and add your API keys and other environment variables:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   RAPIDAPI_KEY=your_rapidapi_key
   TAVILY_API_KEY=your_tavily_api_key
   BRAVE_SEARCH_API=your_brave_search_api_key
   DATABASE_URL=your_database_url
   ```

3. **Build and Start the Docker Containers**:

   ```bash
   docker-compose up --build
   ```

### Running the Application

Once the Docker containers are up and running, access the application at `http://localhost:8002` in your web browser.

## Usage

- **Start a Chat**: Begin by entering your travel-related query in the chat interface.
- **Receive Recommendations**: Weir will process your query and provide recommendations for flights, hotels, and destinations.
- **Refine Your Search**: You can refine your search by providing additional details or constraints.

## Configuration

- **Logstash and Elasticsearch**: Weir uses Logstash and Elasticsearch for logging and data storage. Ensure the certificates are correctly configured for secure communication.
- **API Keys**: Ensure your API keys are set in the `.env` file for accessing external services.

## Architecture

The application is built using a microservices architecture with the following components:

- **App Service**: The main application logic and chat interface.
- **Logstash**: Collects and processes logs from the application.
- **Elasticsearch**: Stores and indexes logs for analysis.
- **PostgreSQL**: Database for storing user data and application state.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [yourname@example.com](mailto:yourname@example.com).

---

Thank you for using Weir! We hope it helps you plan your next adventure with ease.
