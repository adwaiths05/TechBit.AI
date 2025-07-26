# TechBit.AI
## Overview
TechBit AI is an innovative AI-powered agent that empowers developers by generating and refining code, curating tech trends, and creating content for Medium and LinkedIn. It executes code until achieving desired outputs, provides explanations with curated learning resources, and automates content posting. This project showcases advanced skills in AI, API integration, and full-stack development, making it a standout portfolio piece.
## **Phase 1**: 
Develop a coding agent that generates and executes code, integrates with the Medium API for content creation, and curates learning resources (e.g., docs, videos, articles).
### Features (Phase 1)

- **Code Generation & Execution**: Generates Python code using CodeLlama, executes it in a sandbox (Pyodide), and refines until the output matches expectations.
- **Explanation & Resources**: Offers code explanations with links to Python Docs, MDN, YouTube tutorials, and Stack Overflow Q&A.
- **Medium Integration**: Drafts and posts coding tutorials to Medium via API.
- **Tech Trend Updates**: Fetches trending topics from GitHub and Hacker News (planned for expansion).
- **Scalable Backend**: Built with FastAPI, hosted on AWS, with Pinecone for resource storage.

## Tech Stack

- **Backend**: Python, FastAPI, PostgreSQL
- **AI**: CodeLlama (Hugging Face), Pyodide
- **APIs**: Medium API, YouTube API, Stack Overflow API, GitHub API
- **Storage**: Pinecone (vector database)
- **Frontend**: React (planned for Phase 2)
- **Cloud**: AWS/GCP

## Setup Instructions
### Clone the Repository:
``` bash
git clone https://github.com/yourusername/techbit-ai.git
cd techbit-ai
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Set Environment Variables:
```bash
Create a .env file with:HF_TOKEN=your_huggingface_token
PINECONE_API_KEY=your_pinecone_api_key
MEDIUM_TOKEN=your_medium_access_token
```

### Run the Application:
```bash
uvicorn main:app --reload
```

### Access: 
Open http://localhost:8000 in your browser (UI planned for Phase 2).

## Usage

- **Code Generation**:
Input a prompt (e.g., "Write a Python function to sort a list").
The agent generates, executes, and refines code until the output matches (e.g., [1, 2, 3] for [3, 1, 2]).


- **Explanation**:
After execution, opt for an explanation with curated resources (e.g., Python Docs, YouTube tutorials).


- **Content Creation**:
Draft a Medium post with the code and explanation, ready to publish.


- **Tech Updates**:
Request summaries of trending tech topics (expanded in future phases).



## Future Phases

Phase 2: Add LinkedIn API for automated posting and networking, build React-based chatbot UI.
Phase 3: Support additional languages (e.g., JavaScript, Java), integrate more resources (e.g., freeCodeCamp, O’Reilly).
Phase 4: Enhance personalization with user profiles and deploy as a SaaS product.

## Contributing
Contributions are welcome! Fork the repo, create a branch, and submit a pull request.

## License
MIT License
