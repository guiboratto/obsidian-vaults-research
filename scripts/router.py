#!/usr/bin/env python3
"""
Query Router for Obsidian Knowledge Base

Routes user questions to appropriate domains and agents.
"""

from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, Any


class ObsidianRouter:
    """Routes questions to appropriate domains and agents."""
    
    def __init__(self, model: str = "llama3.2"):
        self.llm = Ollama(model=model)
        self.router_chain = None
        self.agent_chain = None
        
        self._initialize_chains()
    
    def _initialize_chains(self):
        """Initialize routing and agent chains."""
        
        # Router prompt
        router_prompt = PromptTemplate(
            template="""You are a domain classifier for an Obsidian knowledge base.

Available Domains:
- 00-Inbox: Quick capture, triage, urgent tasks
- 01-Projects: Time-bound work with specific goals and deadlines
- 02-Areas: Ongoing responsibilities and domains
- 03-Resources: Reference material, documentation, tools
- 02-Shared-Knowledge: Cross-domain insights, ideas, frameworks
- 05-Work-System: PM workflows, meetings, decisions, OKRs
- 06-Personal: Personal life, journaling, habits, memories
- 07-Agents: AI agent definitions and configurations

When classifying, consider:
1. The subject matter (projects, personal, work, research, etc.)
2. The intent (capture, planning, review, analysis, etc.)
3. The time horizon (immediate, short-term, long-term)
4. The workflow (GTD, PM, creative, etc.)

Question: {question}

Respond with a JSON object:
{{
  "domain": "DOMAIN_NAME",
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation",
  "suggested_agent": "AGENT_NAME or null"
}}

Domain names must be exactly one of: 00-Inbox, 01-Projects, 02-Areas, 03-Resources, 02-Shared-Knowledge, 05-Work-System, 06-Personal, 07-Agents

Agent names (optional): PM-Agent, Research-Agent, Creative-Agent, Personal-Agent
""",
            input_variables=["question"]
        )
        
        self.router_chain = LLMChain(llm=self.llm, prompt=router_prompt)
    
    def route(self, question: str) -> Dict[str, Any]:
        """Route a question to the appropriate domain."""
        result = self.router_chain.run(question=question)
        
        # Parse JSON response
        try:
            # Extract JSON from response (in case there's extra text)
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                result = json_match.group(0)
            
            routing = json.loads(result)
            return routing
        except Exception as e:
            print(f"Error parsing routing result: {e}")
            print(f"Raw result: {result}")
            return {
                "domain": "02-Shared-Knowledge",
                "confidence": 0.5,
                "reasoning": "Default to shared knowledge on parse error",
                "suggested_agent": null
            }
    
    def get_domain_description(self, domain: str) -> str:
        """Get description of a domain."""
        descriptions = {
            "00-Inbox": "Quick capture, triage, urgent tasks",
            "01-Projects": "Time-bound work with specific goals and deadlines",
            "02-Areas": "Ongoing responsibilities and domains",
            "03-Resources": "Reference material, documentation, tools",
            "02-Shared-Knowledge": "Cross-domain insights, ideas, frameworks",
            "05-Work-System": "PM workflows, meetings, decisions, OKRs",
            "06-Personal": "Personal life, journaling, habits, memories",
            "07-Agents": "AI agent definitions and configurations"
        }
        return descriptions.get(domain, "Unknown domain")


def main():
    """Test the router."""
    router = ObsidianRouter()
    
    test_questions = [
        "What should I work on today?",
        "I need to plan my project launch",
        "I'm thinking about new ideas for my business",
        "How do I structure meeting notes?",
        "What's my reading list?",
        "I need to review my habits"
    ]
    
    print("Testing Query Router")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        routing = router.route(question)
        
        print(f"  Domain: {routing.get('domain')}")
        print(f"  Confidence: {routing.get('confidence')}")
        print(f"  Agent: {routing.get('suggested_agent') or 'None'}")
        print(f"  Reasoning: {routing.get('reasoning')}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
