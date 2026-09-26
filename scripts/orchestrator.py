#!/usr/bin/env python3
"""
LangChain Orchestrator for Obsidian Knowledge Base

Combines routing, context loading, and agent activation into a unified system.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain.schema import Document
except ImportError as e:
    print(f"Error importing required packages: {e}")
    exit(1)


class ObsidianOrchestrator:
    """Orchestrates the entire Obsidian knowledge base system."""
    
    def __init__(
        self,
        vault_path: str = "./unified-brain",
        chroma_path: str = "./chromadb",
        model: str = "llama3.2"
    ):
        self.vault_path = Path(vault_path)
        self.chroma_path = Path(chroma_path)
        self.model = model
        
        # Initialize components
        self.router = None
        self.vectorstore = None
        self.embeddings = None
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize router and vector store."""
        print("Initializing Orchestrator...")
        
        # Initialize embeddings
        print("Loading Ollama embeddings...")
        self.embeddings = OllamaEmbeddings(model=self.model)
        
        # Initialize vector store
        print("Loading ChromaDB...")
        self.vectorstore = Chroma(
            persist_directory=str(self.chroma_path),
            embedding_function=self.embeddings
        )
        
        # Initialize router
        print("Initializing query router...")
        from router import ObsidianRouter
        self.router = ObsidianRouter(model=self.model)
        
        print("✓ Orchestrator initialized")
    
    def load_context(
        self,
        question: str,
        domain: str,
        top_k: int = 10,
        use_semantic: bool = True
    ) -> List[Document]:
        """Load relevant documents based on domain and question."""
        
        if use_semantic:
            # Semantic search with domain filter
            results = self.vectorstore.similarity_search(
                question,
                k=top_k,
                filter={"folder": domain}
            )
        else:
            # Pure domain filter (no semantic search)
            results = self.vectorstore.similarity_search_with_score(
                "",
                k=top_k,
                filter={"folder": domain}
            )
            results = [r[0] for r in results]
        
        return results
    
    def activate_agent(self, question: str, context_docs: List[Document]) -> str:
        """Activate appropriate agent and generate response."""
        
        # Detect agent type from question and context
        agent_type = self._detect_agent_type(question, context_docs)
        
        # Load agent instructions
        agent_file = self.vault_path / "07-Meta" / f"{agent_type}-Agent.md"
        
        if agent_file.exists():
            agent_instructions = agent_file.read_text(encoding='utf-8')
        else:
            agent_instructions = self._get_default_agent_instructions(agent_type)
        
        # Prepare context
        context_text = "\n\n".join([
            f"=== Document {i+1} ===\n{doc.page_content}"
            for i, doc in enumerate(context_docs)
        ])
        
        # Build prompt
        prompt = self._build_agent_prompt(
            agent_instructions,
            context_text,
            question
        )
        
        # Generate response
        from langchain.llms import Ollama
        llm = Ollama(model=self.model)
        response = llm.predict(prompt)
        
        return response
    
    def _detect_agent_type(self, question: str, context_docs: List[Document]) -> str:
        """Detect which agent should handle the question."""
        
        # Check for agent-specific keywords
        agent_keywords = {
            "PM-Agent": ["project", "meeting", "decision", "OKR", "initiative", "roadmap"],
            "Research-Agent": ["framework", "methodology", "best practice", "research", "study"],
            "Creative-Agent": ["idea", "brainstorm", "creative", "write", "draft"],
            "Personal-Agent": ["journal", "habit", "personal", "life", "health"]
        }
        
        question_lower = question.lower()
        
        for agent, keywords in agent_keywords.items():
            for keyword in keywords:
                if keyword in question_lower:
                    return agent
        
        # Default to PM-Agent if uncertain
        return "PM-Agent"
    
    def _get_default_agent_instructions(self, agent_type: str) -> str:
        """Get default agent instructions if file doesn't exist."""
        default_instructions = {
            "PM-Agent": """You are a Product Manager Assistant.

You help with:
- Project planning and tracking
- Meeting preparation and note-taking
- Decision documentation
- OKR and initiative management
- Strategic thinking and prioritization

Guidelines:
1. Use templates from the vault structure
2. Maintain consistent formatting
3. Reference specific notes with wiki-links [[note-name]]
4. Keep responses actionable and practical
5. Focus on outcomes and next steps

Your responses should be structured, clear, and actionable.""",

            "Research-Agent": """You are a Research Assistant.

You help with:
- Framework and methodology explanations
- Best practice recommendations
- Comparative analysis
- Knowledge synthesis
- Cross-domain insights

Guidelines:
1. Ground responses in the knowledge base
2. Cite sources with wiki-links [[note-name]]
3. Provide balanced, evidence-based answers
4. Highlight trade-offs and considerations
5. Suggest next steps for deeper exploration

Your responses should be thorough, well-structured, and referenceable.""",

            "Creative-Agent": """You are a Creative Writing Assistant.

You help with:
- Idea generation and brainstorming
- Drafting and refining content
- Creative problem solving
- Lateral thinking exercises
- Story and narrative development

Guidelines:
1. Encourage creative and unconventional thinking
2. Provide multiple perspectives
3. Use analogies and metaphors
4. Keep tone engaging and inspiring
5. Offer actionable creative directions

Your responses should be imaginative, inspiring, and creative.""",

            "Personal-Agent": """You are a Personal Assistant.

You help with:
- Journaling and reflection
- Habit tracking and improvement
- Personal goal setting
- Health and wellness
- Life organization

Guidelines:
1. Be supportive and understanding
2. Focus on personal growth and well-being
3. Provide practical, actionable advice
4. Maintain privacy and confidentiality
5. Encourage self-reflection

Your responses should be personal, supportive, and growth-oriented."""
        }
        
        return default_instructions.get(agent_type, "You are a helpful AI assistant.")
    
    def _build_agent_prompt(
        self,
        agent_instructions: str,
        context_text: str,
        question: str
    ) -> str:
        """Build the complete agent prompt."""
        
        prompt = f"""{agent_instructions}

Context from Knowledge Base:
{context_text}

User Question:
{question}

Your Response:
"""
        
        return prompt
    
    def answer(self, question: str) -> Dict[str, Any]:
        """Answer a question using the full pipeline."""
        
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print('='*60)
        
        # Step 1: Route the question
        print("\n[1/3] Routing question...")
        routing = self.router.route(question)
        
        domain = routing.get("domain", "02-Shared-Knowledge")
        confidence = routing.get("confidence", 0.5)
        agent = routing.get("suggested_agent") or self._detect_agent_type(question, [])
        
        print(f"  Domain: {domain}")
        print(f"  Confidence: {confidence:.2f}")
        print(f"  Agent: {agent}")
        
        # Step 2: Load context
        print(f"\n[2/3] Loading context from {domain}...")
        context_docs = self.load_context(question, domain, top_k=5)
        print(f"  Loaded {len(context_docs)} documents")
        
        # Step 3: Generate response
        print(f"\n[3/3] Generating response...")
        response = self.activate_agent(question, context_docs)
        
        result = {
            "question": question,
            "domain": domain,
            "confidence": confidence,
            "agent": agent,
            "context_count": len(context_docs),
            "response": response
        }
        
        return result
    
    def run_interactive(self):
        """Run in interactive mode."""
        print("\nObsidian Knowledge Base - Interactive Mode")
        print("Type your question or 'quit' to exit\n")
        
        while True:
            try:
                question = input("You: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\nGoodbye!")
                    break
                
                if not question:
                    continue
                
                result = self.answer(question)
                
                print(f"\n{'='*60}")
                print("Response:")
                print('='*60)
                print(result["response"])
                print(f"\nSources: {result['context_count']} documents")
                print('='*60)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                import traceback
                traceback.print_exc()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Obsidian Knowledge Base Orchestrator")
    parser.add_argument("--vault", default="./unified-brain", help="Path to unified vault")
    parser.add_argument("--chroma", default="./chromadb", help="Path to ChromaDB")
    parser.add_argument("--model", default="llama3.2", help="Ollama model to use")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--question", help="Answer a single question")
    
    args = parser.parse_args()
    
    orchestrator = ObsidianOrchestrator(
        vault_path=args.vault,
        chroma_path=args.chroma,
        model=args.model
    )
    
    if args.interactive:
        orchestrator.run_interactive()
    elif args.question:
        result = orchestrator.answer(args.question)
        print(result["response"])
    else:
        print("Run with --interactive for chat mode or --question 'your question' for single question")


if __name__ == "__main__":
    main()
