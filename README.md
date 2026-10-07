# python-openrouter-agent
OpenRouter + Python Agent
             ┌───────────────┐
             │   OpenRouter  │
             │      LLM      │
             └───────┬───────┘
                     │
                Tool request
                     ↓
              calculate()
                     ↓
                   150
                     │
                     ↓
             ┌───────────────┐
             │   OpenRouter  │
             │      LLM      │
             └───────┬───────┘
                     │
                Tool request
                     ↓
              calculate()
                     ↓
                  1500
                     │
                     ↓
                   Answer



V1  ✅ OpenRouter + Python Agent
     └── Calculator Tool

V2  → Multiple Tools
     ├── Calculator
     ├── Date/Time
     └── File Reader

V3  → Tool Registry
     └── Automatically register tools

V4  → Agent Memory
     └── Remember previous conversation

V5  → RAG Tool
     └── LanceDB + embeddings

V6  → Web Search Tool

V7  → Agent → Agent
     ├── Research Agent
     ├── RAG Agent
     └── Calculation Agent

V8  → Advanced autonomous Agent
     └── Planning → Tools → Verification → Answer