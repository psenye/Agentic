# Financial Decision-Making System with GPT-4o and Agentic Automation

## Overview

This repository contains the code for a financial decision-making system that automates the generation of financial surveys, simulates investor responses, and provides personalized financial advice using GPT-4o and Agentic Automation. The system integrates virtual personas, tailored survey templates, and Retrieval-Augmented Generation (RAG) for enhanced decision-making accuracy.

The framework leverages **multiple agents** to perform tasks such as creating virtual personas (Agent-C), generating survey templates (Agent-S), simulating responses (Agent-0 to Agent-(n-1)), and analyzing responses to generate financial recommendations (Agent-E). This innovative system simulates real-world financial decision-making, allowing virtual agents to act as real investors in financial contexts.

## Features

- **Agentic Automation**: Simulate investor behavior with virtual personas based on GPT-4o and RAG.
- **Survey Generation**: Automatically generate financial surveys tailored to different investor profiles.
- **Response Simulation**: Virtual agents simulate responses reflecting diverse investment preferences and risk profiles.
- **Decision-Making**: Aggregated responses are analyzed and used to generate personalized financial advice.
- **Scalability**: The system supports the parallel execution of multiple virtual personas to simulate real-world financial scenarios.
  
## Installation

### Requirements

- Python 3.8+
- GPT-4o API access (from OpenAI or your preferred platform)
- Azure AI Foundry (for RAG, GPT-4o, and Azure AI Search services)

### Setup

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/financial-decision-making.git
   cd financial-decision-making
   ```

2. **Install dependencies**:
   Use pip to install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Azure AI Foundry Configuration**:
   Set up your Azure AI Foundry credentials. You'll need access to **Azure AI Search** and **GPT-4o API** through Azure.
   Add the necessary credentials in a `.env` file:
   ```bash
   GPT4_API_KEY="your_api_key_here"
   AZURE_SEARCH_KEY="your_azure_search_key_here"
   AZURE_AI_FOUNDRY_ENDPOINT="your_azure_ai_foundry_endpoint"
   ```

4. **Run the application**:
   Start the agent system and run the survey and decision-making simulation:
   ```bash
   python run_simulation.py
   ```

## Usage

This project allows you to simulate various investor personas, run financial surveys, and generate actionable financial advice.

- **Create Virtual Personas**: Use Agent-C to generate multiple investor profiles.
- **Generate Survey Templates**: Agent-S will create tailored financial surveys based on the personas.
- **Simulate Responses**: Virtual agents (Agent-0 to Agent-(n-1)) simulate responses based on the generated surveys.
- **Analyze and Make Decisions**: Agent-E aggregates the responses and uses decision-making models to generate financial recommendations.

## Contributing

Feel free to fork this repository, open issues, and submit pull requests. If you have suggestions for improvements or additions, please contribute to this project.

### Steps to contribute:

1. Fork this repository.
2. Create a new branch for your changes.
3. Make the changes and commit them with clear messages.
4. Push your changes and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI’s **GPT-4o** for providing advanced language modeling capabilities.
- **Azure AI Foundry** for providing the infrastructure and services that enable RAG and GPT-4o integration.
- Azure AI **Search** and **text-embedding-ada-002** for facilitating efficient search and data processing.
- Special thanks to the community and contributors who helped refine this system.

## Contact

For any questions or issues, please open an issue in the repository or contact the repository owner directly.
