ARCH-002: Agent Interaction Diagram (placeholder)

This file is a textual placeholder for ARCH-002 Agent Interaction Diagram. Add the final diagram image at docs/architecture/ARCH-002_agent_interaction.png

Summary:
- Agent roles: Ingest Agent, Partitioner Agent, Annotator Agent (KEGG adapter), Execution Agent (worker pool), Reviewer Agent (human-in-loop gate), Audit Agent (GPG logger)
- Message flows are serialized and signed at each critical transition (per SEC-001)
