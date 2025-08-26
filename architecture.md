# DeepJudge Multi-Agent System - Architecture Documentation

## System Architecture Overview

```mermaid
C4Context
    title DeepJudge Multi-Agent System Context Diagram
    
    Person(user, "Legal Professional", "Queries legal documents for target companies and law firms")
    System(deepjudge, "DeepJudge Multi-Agent System", "3-step LLM workflow for law firm identification")
    System_Ext(openai, "OpenAI API", "Provides gpt-4o-mini model with temperature 0.2")
    
    Rel(user, deepjudge, "Submits query + document paragraphs")
    Rel(deepjudge, openai, "Processes text via LLM calls")
    Rel(deepjudge, user, "Returns structured JSON results")
```

## Container Diagram

```mermaid
C4Container
    title DeepJudge Multi-Agent System - Container View
    
    Container_Boundary(system, "DeepJudge System") {
        Container(orchestrator, "Multi-Agent Orchestrator", "Python", "Coordinates 3-step workflow")
        Container(llm1, "LLM1 Agent", "Python", "Target company detection")
        Container(llm2, "LLM2 Agent", "Python", "Law firm extraction")
        Container(llm3, "LLM3 Agent", "Python", "JSON compilation")
        ContainerDb(data, "Result Storage", "Python Objects", "Stores analyses and outputs")
    }
    
    System_Ext(openai, "OpenAI API")
    Person(user, "Legal Professional")
    
    Rel(user, orchestrator, "Query + Paragraphs")
    Rel(orchestrator, llm1, "Step 1")
    Rel(orchestrator, llm2, "Step 2") 
    Rel(orchestrator, llm3, "Step 3")
    Rel(llm1, openai, "API Call")
    Rel(llm2, openai, "API Call")
    Rel(llm3, openai, "API Call")
    Rel(orchestrator, data, "Store Results")
```

## Workflow Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant O as Orchestrator
    participant L1 as LLM1 Agent
    participant L2 as LLM2 Agent
    participant L3 as LLM3 Agent
    participant API as OpenAI API
    
    U->>O: Submit query + paragraphs
    
    Note over O,L1: Step 1: Target Company Detection
    O->>L1: Process user query
    L1->>API: Analyze for target company
    API-->>L1: Target company result
    
    alt Target Company Found
        L1-->>O: "The target company is [NAME]"
        
        Note over O,L2: Step 2: Paragraph Analysis
        loop For each paragraph
            O->>L2: Analyze paragraph + target company
            L2->>API: Extract law firm information
            API-->>L2: Law firm analysis
            L2-->>O: Structured analysis result
        end
        
        Note over O,L3: Step 3: JSON Compilation
        O->>L3: Compile all analyses
        L3->>API: Generate final JSON
        API-->>L3: Structured JSON
        L3-->>O: Final JSON result
        
        O-->>U: Complete results with JSON
    else No Target Company
        L1-->>O: "<user_message>Query not relevant</user_message>"
        O-->>U: Irrelevant query message
    end
```

## Component Architecture

```mermaid
classDiagram
    class MultiAgentOrchestrator {
        +llm1: LLM1Agent
        +llm2: LLM2Agent  
        +llm3: LLM3Agent
        +process(query, paragraphs) Dict
    }
    
    class LLMAgent {
        <<abstract>>
        +client: OpenAI
        +model: str
        +temperature: float
        +query(system_prompt, user_message) str
    }
    
    class LLM1Agent {
        +system_prompt: str
        +process(user_query) str
    }
    
    class LLM2Agent {
        +system_prompt: str
        +process(paragraph, target_company) str
    }
    
    class LLM3Agent {
        +system_prompt: str
        +process(analyses) str
    }
    
    class ParagraphAnalysis {
        +buyer_firm: str
        +seller_firm: str
        +third_party: str
        +contains_target: bool
    }
    
    class FinalOutput {
        +buyer_firm: str
        +seller_firm: str
        +third_party: str
        +contains_target_firm: bool
    }
    
    MultiAgentOrchestrator --> LLM1Agent
    MultiAgentOrchestrator --> LLM2Agent
    MultiAgentOrchestrator --> LLM3Agent
    
    LLM1Agent --|> LLMAgent
    LLM2Agent --|> LLMAgent
    LLM3Agent --|> LLMAgent
    
    MultiAgentOrchestrator ..> ParagraphAnalysis
    MultiAgentOrchestrator ..> FinalOutput
```

## Data Flow Architecture

```mermaid
flowchart TD
    A[User Query + Paragraphs] --> B{LLM1: Target Company Detection}
    
    B -->|No Target Found| C[Return: user_message XML]
    B -->|Target Found| D[Extract Target Company Name]
    
    D --> E[LLM2: Process Each Paragraph]
    E --> F[Paragraph 1 Analysis]
    E --> G[Paragraph 2 Analysis] 
    E --> H[Paragraph 3 Analysis]
    E --> I[Paragraph 4 Analysis]
    
    F --> J[LLM3: Compile All Analyses]
    G --> J
    H --> J
    I --> J
    
    J --> K[Generate Final JSON]
    K --> L{JSON Valid?}
    
    L -->|Yes| M[Return Complete Results]
    L -->|No| N[Return Error + Raw Output]
    
    style A fill:#e1f5fe
    style C fill:#ffebee
    style M fill:#e8f5e8
    style N fill:#fff3e0
```

## System Prompts Architecture

```mermaid
mindmap
  root((System Prompts))
    LLM1 Prompt
      Target Detection
        Company Identification
        XML Format Response
        Relevance Checking
    LLM2 Prompt
      Law Firm Extraction
        Buyer Representative
        Seller Representative  
        Third Party Firms
        Target Presence Check
    LLM3 Prompt
      JSON Compilation
        Data Aggregation
        Default Values
        Structured Output
        Validation Rules
```

## Error Handling Flow

```mermaid
flowchart TD
    A[Process Request] --> B{LLM1 Success?}
    B -->|No| C[Return API Error]
    B -->|Yes| D{Target Found?}
    
    D -->|No| E[Return user_message]
    D -->|Yes| F[Process Paragraphs]
    
    F --> G{LLM2 Success?}
    G -->|No| H[Return Analysis Error]
    G -->|Yes| I[Compile Results]
    
    I --> J{LLM3 Success?}
    J -->|No| K[Return Compilation Error]
    J -->|Yes| L{JSON Valid?}
    
    L -->|No| M[Return Parse Error + Raw]
    L -->|Yes| N[Return Success]
    
    style C fill:#ffcdd2
    style H fill:#ffcdd2
    style K fill:#ffcdd2
    style M fill:#ffcdd2
    style N fill:#c8e6c9
```

## API Integration Pattern

```mermaid
sequenceDiagram
    participant Agent as LLM Agent
    participant Client as OpenAI Client
    participant API as OpenAI API
    
    Agent->>Client: Create completion request
    Client->>API: POST /v1/chat/completions
    
    Note over API: Model: gpt-4o-mini<br/>Temperature: 0.2
    
    API-->>Client: Response with content
    Client-->>Agent: Parsed response text
    
    Agent->>Agent: Process and validate response
    Agent-->>Agent: Return structured result
```