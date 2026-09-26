# Obsidian-to-Hermes Integration Plan
## Unified "Super Brain" Architecture

**Goal:** Integrate multiple Obsidian vaults into a single, AI-native knowledge system that Hermes can read, query, and extend.

**Target Date:** 2026-09-25
**Status:** Planning Phase

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Hermes Telegram Gateway                   │
│              (Control Plane + User Interface)                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ LangChain (Ollama)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              LangChain Orchestrator Layer                    │
│  - Query router (domain detection)                          │
│  - Context loader (relevant vaults)                         │
│  - Knowledge graph linker (cross-vault connections)         │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Vault A:     │ │ Vault B:     │ │ Vault C:     │
│ Work Vault   │ │ Second Brain │ │ PARA+GTD     │
│ (lukeinglis) │ │ (project)    │ │ (timominkus) │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
           ┌──────────────────────────┐
           │  ChromaDB Vector Store   │
           │  - Embeddings of all docs │
           │  - Semantic search        │
           │  - Cross-vault retrieval  │
           └──────────────────────────┘
```

---

## Phase 1: Vault Consolidation (Week 1)

### 1.1 Create Unified Vault Structure
**Source vaults:**
- `lukeinglis/work-vault` (PM workflows, meetings, decisions)
- `Second Brain project vault` (general second brain)
- `timominkus/obsidian-para-gtd-ai` (PARA + GTD system)
- `420Hippie/vault-structure` (multi-venture, agent routing)

**Target structure:**
```
unified-brain/
├── 00-Inbox/                    # Quick capture (GTD-style)
├── 01-Active/                   # Operational layer
│   ├── 01-Projects/             # Time-bound work
│   ├── 02-Areas/                # Ongoing responsibilities
│   ├── 03-Resources/            # Reference material
│   └── 04-Inbox-Processed/      # Weekly processed items
├── 02-Shared-Knowledge/         # Cross-vault layer
│   ├── 01-Ideas/                # Long-horizon thinking
│   ├── 02-Books/                # Reading notes
│   ├── 03-Research/             # Synthesized knowledge
│   ├── 04-Frameworks/           # Patterns and methodologies
│   └── 05-Resources/            # Tools and references
├── 03-Work-System/              # PM-specific workflows
│   ├── 01-Meetings/             # Meeting notes
│   ├── 02-Decisions/            # Decision records
│   ├── 03-Initiatives/          # Time-bound projects
│   ├── 04-OKRs/                 # Goal tracking
│   └── 05-Weekly-Rhythm/        # Weekly planning/review
├── 04-Personal/                 # Personal domain
│   ├── 01-Journal/              # Daily/weekly journal
│   ├── 02-Blog/                 # Writing drafts
│   ├── 03-Habits/               # Habit tracking
│   └── 04-Memories/             # Personal history
├── 05-Agents/                   # AI agent definitions
│   ├── 01-PM-Agent/             # Product Manager persona
│   ├── 02-Research-Agent/       # Research synthesizer
│   ├── 03-Writing-Agent/        # Content writer
│   └── 04-Creative-Agent/       # Brainstorming
├── 06-Templates/                # Note templates
├── 07-Meta/                     # Vault configuration
│   ├── 01-CLAUDE.md             # AI context specification
│   ├── 02-MEMORY.md             # Memory index
│   ├── 03-Agent-Roster.md       # Agent definitions
│   ├── 04-Workflows.md          # Process documentation
│   └── 05-Integration-Guide.md  # Hermes integration guide
└── 08-Archive/                  # Retired content
```

**Key conventions:**
- Numbered folders (`00-XX`) for stable ordering
- Kebab-case filenames
- YAML frontmatter with `type`, `status`, `created`, `updated`, `tags`
- Wiki-links `[[note-name]]` for cross-referencing
- Date prefixes for temporal notes (`YYYY-MM-DD`)

### 1.2 Import Existing Content
**Process:**
1. Open each source vault in Obsidian
2. Use Templater to apply new templates to existing notes
3. Use `obsidian-importer` plugin to bulk move files
4. Run automated script to:
   - Add YAML frontmatter to all notes
   - Normalize wiki-links
   - Create cross-references
   - Populate shared knowledge from all vaults

**Script:** `scripts/import-vaults.js`
- Reads source vaults
- Applies templates
- Updates frontmatter
- Normalizes links
- Generates index files

---

## Phase 2: Vector Database Setup (Week 2)

### 2.1 ChromaDB Integration
**Install:**
```bash
pip install chromadb langchain-community langchain-ollama
```

**Embedding model:**
- Use Ollama `llama3.2` (7B) for embeddings
- Local, private, fast
- Or use `nomic-embed-text` if needed

**Setup script:** `scripts/setup-chromadb.py`
```python
from chromadb import PersistentClient
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import ObsidianLoader

# Initialize ChromaDB
client = PersistentClient(path="./chromadb")
collection = client.get_or_create_collection("obsidian-brain")

# Load all markdown files
loader = ObsidianLoader("./unified-brain", glob="**/*.md")
docs = loader.load()

# Create embeddings
embeddings = OllamaEmbeddings(model="llama3.2")
texts = [doc.page_content for doc in docs]
metadatas = [{"source": doc.metadata.get("path", "")} for doc in docs]

# Add to ChromaDB
collection.add(
    documents=texts,
    metadatas=metadatas,
    ids=[f"doc_{i}" for i in range(len(texts))]
)
```

### 2.2 Index Structure
**Collections:**
1. `obsidian-brain` — All documents (full-text search)
2. `obsidian-themes` — Only notes with `#theme` tag
3. `obsidian-projects` — Only project-related notes
4. `obsidian-meetings` — Only meeting notes
5. `obsidian-decisions` — Only decision records

**Metadata schema:**
```json
{
  "path": "00-Inbox/2026-09-25.md",
  "type": "daily-note",
  "status": "active",
  "tags": ["gtd", "capture", "daily"],
  "folder": "00-Inbox",
  "created": "2026-09-25",
  "updated": "2026-09-25",
  "agent": "none"
}
```

---

## Phase 3: LangChain Orchestration (Week 3)

### 3.1 Query Router
**Function:** Detect which domain the user is asking about and route to appropriate vault section.

```python
# router.py
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = Ollama(model="llama3.2")

router_prompt = PromptTemplate(
    template="""
    Given the user's question, determine which domain it belongs to:

    Domains:
    - 00-Inbox: Quick capture, triage
    - 01-Projects: Time-bound work with deadlines
    - 02-Areas: Ongoing responsibilities
    - 03-Resources: Reference material
    - 04-Shared-Knowledge: Cross-domain insights
    - 05-Work-System: PM workflows, meetings, decisions
    - 06-Personal: Personal life, journal, habits

    Question: {question}

    Domain: [DOMAIN]
    """,
    input_variables=["question"]
)

router_chain = LLMChain(llm=llm, prompt=router_prompt)
```

### 3.2 Context Loader
**Function:** Load relevant documents from ChromaDB based on:
1. Domain routing
2. Semantic search (vector similarity)
3. Cross-references (wiki-links)

```python
# context_loader.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

vectorstore = Chroma(
    persist_directory="./chromadb",
    embedding_function=OllamaEmbeddings(model="llama3.2")
)

def load_context(question, domain=None, top_k=10):
    if domain:
        # Filter by folder
        results = vectorstore.similarity_search(
            question,
            k=top_k,
            filter={"folder": domain}
        )
    else:
        # Full semantic search
        results = vectorstore.similarity_search(question, k=top_k)

    return results
```

### 3.3 Agent Orchestration
**Function:** Activate appropriate agent persona based on context.

**Agent definitions:**

1. **PM Agent** (`06-Personal/01-Journal/PM-Agent.md`):
   - Activated when asking about: projects, decisions, meetings, OKRs
   - Uses templates from `03-Work-System/`
   - Maintains decision logs and meeting notes

2. **Research Agent** (`06-Personal/01-Journal/Research-Agent.md`):
   - Activated when asking about: frameworks, methodologies, best practices
   - Uses templates from `02-Shared-Knowledge/`
   - Synthesizes knowledge from multiple sources

3. **Creative Agent** (`06-Personal/01-Journal/Creative-Agent.md`):
   - Activated when asking about: ideas, brainstorming, creative writing
   - Uses templates from `02-Shared-Knowledge/01-Ideas/`
   - Applies lateral thinking techniques

4. **Personal Agent** (`06-Personal/01-Journal/Personal-Agent.md`):
   - Activated for personal questions, journaling, habits
   - Uses templates from `04-Personal/`

**Agent activation logic:**
```python
def activate_agent(question, context):
    # Analyze question and context
    agent_type = detect_agent_type(question, context)

    # Load agent-specific instructions
    agent_file = f"06-Personal/01-Journal/{agent_type}-Agent.md"
    agent_context = load_file(agent_file)

    # Load relevant documents
    docs = load_context(question, top_k=5)

    # Build prompt
    prompt = f"""
    You are the {agent_type} Agent.

    Agent Context:
    {agent_context}

    Relevant Knowledge:
    {docs}

    User Question:
    {question}

    Your Response:
    """

    return llm.predict(prompt)
```

---

## Phase 4: Hermes Integration (Week 4)

### 4.1 Telegram Bot Setup
**Install:**
```bash
pip install python-telegram-bot langchain-telegram-bot
```

**Bot structure:**
```python
# hermes_bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт! Я твоій Obsidian-мозок. Запитай щось про твої проекти, рішення, зустрічі або ідеї."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text

    # Route to appropriate agent
    agent_response = orchestrate_response(question)

    await update.message.reply_text(agent_response)

app = ApplicationBuilder().token("HERMES_BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
```

### 4.2 Prompt Engineering
**System prompt for Hermes:**
```
You are Hermes, an AI assistant powered by a unified Obsidian knowledge base.

Your Knowledge Base:
- Unified vault with 8 main domains (00-07)
- Vector database (ChromaDB) with 10,000+ documents
- Agent personas for different workflows

When answering:
1. First, identify the domain relevant to the question
2. Load relevant documents from ChromaDB
3. Activate the appropriate agent persona
4. Use templates and conventions from your vault
5. Reference specific notes with wiki-links [[note-name]]
6. Maintain consistency with existing structure

Vault Structure:
- 00-Inbox: Quick capture
- 01-Active: Projects, Areas, Resources
- 02-Shared-Knowledge: Ideas, Books, Research
- 03-Work-System: Meetings, Decisions, OKRs
- 04-Personal: Journal, Blog, Habits
- 05-Agents: AI agent definitions
- 06-Templates: Note templates
- 07-Meta: Configuration, guides

Conventions:
- Use wiki-links [[note-name]] for cross-references
- Add YAML frontmatter to new notes
- Follow numbered folder structure
- Use consistent naming (kebab-case)
- Tag notes appropriately (#tag)
```

### 4.3 Real-time Sync
**Mechanism:** Obsidian Git + ChromaDB sync

1. **Obsidian Git** (automatic):
   - Push changes to GitHub
   - Trigger ChromaDB update on push

2. **ChromaDB sync script:**
```python
# scripts/update-chromadb.py
import subprocess
import time

def sync_obsidian_to_chromadb():
    # Pull latest from Obsidian Git
    subprocess.run(["git", "pull", "origin", "main"])

    # Rebuild ChromaDB
    subprocess.run(["python", "scripts/setup-chromadb.py"])

    # Notify Hermes
    send_telegram_message("🔄 Obsidian brain synced to ChromaDB")

# Run every 5 minutes
while True:
    sync_obsidian_to_chromadb()
    time.sleep(300)
```

---

## Phase 5: Testing & Optimization (Week 5)

### 5.1 Testing Checklist

**Functionality tests:**
- [ ] Query routing to correct domain
- [ ] Context loading from ChromaDB
- [ ] Agent activation based on question
- [ ] Wiki-link generation
- [ ] Template application
- [ ] Real-time sync from Obsidian
- [ ] Telegram bot responsiveness

**Performance tests:**
- [ ] Query latency < 2 seconds
- [ ] ChromaDB indexing speed
- [ ] Memory usage under load
- [ ] Bot uptime (target: 99.9%)

**Quality tests:**
- [ ] Response relevance
- [ ] Consistency with vault structure
- [ ] Template compliance
- [ ] Cross-referencing accuracy

### 5.2 Optimization Targets

**Latency:**
- Query routing: < 500ms
- Context loading: < 1s
- Total response time: < 3s

**Accuracy:**
- Semantic search recall: > 90%
- Domain classification: > 95%
- Wiki-link generation: 100%

**Reliability:**
- ChromaDB sync success rate: 100%
- Bot uptime: 99.9%
- Error handling: Graceful degradation

---

## Phase 6: Documentation & Handoff (Week 6)

### 6.1 Documentation Files

Create in `07-Meta/`:
1. **ARCHITECTURE.md** — System architecture diagram and decisions
2. **INTEGRATION-GUIDE.md** — Setup instructions for new users
3. **API-REFERENCE.md** — ChromaDB query syntax
4. **AGENT-GUIDE.md** — Agent persona definitions and usage
5. **TROUBLESHOOTING.md** — Common issues and solutions
6. **CONTRIBUTION.md** — How to add new notes/templates

### 6.2 Training Materials

1. **User guide** (Telegram bot help messages)
2. **Admin guide** (How to manage the system)
3. **Developer guide** (How to extend agents)

---

## Dependencies & Requirements

### Software
- Obsidian (latest version)
- Python 3.11+
- ChromaDB
- LangChain
- Ollama (local LLM)
- python-telegram-bot

### Hardware
- RAM: 8GB minimum, 16GB recommended
- Storage: 50GB for vault + ChromaDB
- CPU: 4 cores minimum

### External Services
- GitHub (for Obsidian Git sync)
- Telegram Bot Token (free)

---

## Success Metrics

**Technical metrics:**
- 10,000+ documents indexed
- 95% query accuracy
- 99.9% uptime
- < 3s response time

**User metrics:**
- Daily active users (Hermes bot)
- Questions answered from vault
- New notes created
- Cross-references generated

**Quality metrics:**
- Template compliance: 100%
- Wiki-link accuracy: 100%
- Consistency with vault structure: 100%

---

## Next Steps

1. **Immediate (today):**
   - Review and approve architecture
   - Set up Obsidion vault structure
   - Install dependencies

2. **This week:**
   - Import existing vaults
   - Set up ChromaDB
   - Create LangChain router

3. **Next week:**
   - Build Hermes bot
   - Test integration
   - Optimize performance

4. **Following week:**
   - Documentation
   - Training
   - Launch

---

## Rollback Plan

If issues arise:
1. **Hermes bot:** Disable via Telegram admin panel
2. **ChromaDB:** Rebuild from last known good commit
3. **Vault:** Revert to previous version via Git
4. **Agents:** Revert to simple rule-based routing

All changes are version-controlled and reversible.

---

**Created:** 2026-09-25
**Author:** Qwen Code + Ivantsi
**Status:** Ready for implementation
