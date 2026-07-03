# Memory Policy

Use two memory systems with different roles:

## 1. Ontology (Canonical Structured Knowledge)
- Use ontology for entities, properties, and relationships.
- Store durable facts such as people, projects, tasks, events, documents, ownership, dependencies, preferences, and status changes in ontology.
- When a structured fact changes, update ontology rather than creating parallel conflicting records elsewhere.

## 2. LanceDB (Long-term Semantic Recall Layer)
- Use LanceDB (via native memory tools) for natural-language summaries, supporting context, rationale, evidence, and fuzzy recall.
- Store short summaries of important interactions, decisions, explanations, and background context that may help with future retrieval.
- Do not store ontology as a second full canonical copy in LanceDB.

## 3. When to write to Ontology
- Write to ontology when the information can be represented as a typed entity, attribute, or relationship.
- Prefer ontology for facts that should remain stable and queryable over time.
- Before creating a new entity, check whether it already exists and update it if appropriate.

## 4. When to write to LanceDB
- Write to LanceDB when the information is unstructured, explanatory, conversational, or useful mainly for semantic similarity search.
- Write a concise summary after important conversations, decisions, or discoveries.
- If a fact was stored in ontology, only write a brief supporting summary to LanceDB when provenance or contextual recall would be useful.

## 5. Avoid Duplication
- Do not store the same information in both systems as equal canonical truth.
- Ontology holds the structured truth.
- LanceDB holds recall-friendly summaries and evidence.
- If uncertain, prefer ontology for facts and LanceDB for context.

## 6. Retrieval Behavior
- Use ontology first for precise factual or relational questions.
- Use LanceDB when searching for similar past discussions, rationale, prior context, or loosely related memories.
- Combine both when needed: ontology for the answer structure, LanceDB for background and evidence.

## 7. Quality Rules
- Do not create duplicate entities.
- Do not write trivial chatter, greetings, or repetitive status updates to LanceDB.
- Do not store speculative or uncertain claims as ontology facts unless clearly marked as tentative.
- Keep LanceDB entries short, specific, and useful for later retrieval.
