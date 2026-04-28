# Design Rationale: Deterministic Reflection Tree
**Role:** Knowledge Engineer Candidate

## 1. Architectural Guardrails Against AI Hallucination
To fulfill the core requirement of a deterministic, non-hallucinating system, I strictly decoupled the psychological data from the runtime logic. 
* **Semantic Constraints:** All user inputs are restricted to fixed choices (A/B/C/D) via numeric indexing. This removes the necessity for an LLM to interpret free-text sentiment at runtime, eliminating interpretation errors.
* **Deterministic Routing:** I utilized a bespoke TSV structure where branching logic (`answer=X:TargetNode`) is executed via hardcoded dictionary lookups. 
* **Data Sanitization:** The Python agent performs an initial load pass that sanitizes missing tabs/None-types and validates the structure, meaning the system will never guess an outcome; it will either map accurately or fail safely.

## 2. Psychological Grounding & Question Design
The tree was designed to navigate the user through three specific psychological spectrums sequentially, avoiding "moralizing" language in favor of "mirroring" language.

* **Axis 1: Locus of Control (Victim vs. Victor):** Drawing from Julian Rotter’s work, the opening questions don't ask "Are you a victim?" but rather examine the user's *instinct* during friction ("When things got difficult, what was your first instinct?"). Options like "Wait for someone to step in" gently identify an external locus without judgment.
* **Axis 2: Orientation (Entitlement vs. Contribution):** Based on Campbell's Psychological Entitlement research, this axis focuses on the *driver* of workplace interactions. Options like "Receiving credit" vs. "Fixing a problem" separate discretionary effort (Citizenship Behavior) from transaction-minded behavior.
* **Axis 3: Radius (Self-Centrism vs. Altrocentrism):** Rooted in Maslow’s Self-Transcendence, the final axis widens the lens. Moving the user from "Myself" to "The team/customer" reframes their daily stress as part of a larger systemic process, culminating in the highest level of professional reflection.

## 3. Trade-offs in Branching Design
I opted for a **convergent-divergent branching model**. Instead of creating 50+ unique dead-end nodes, the tree branches sharply at the `decision` nodes to provide tailored reflection, and then converges back at `bridge` nodes to move to the next psychological axis. 
* *Trade-off:* This sacrifices hyper-personalization across the entire journey.
* *Benefit:* It ensures the user always hits all three psychological axes within 3-5 minutes, which is critical for an end-of-day tool where user fatigue is high.

## 4. Future Improvements
Given more time, I would:
1. **Implement State Persistence:** Save the end-of-day signals to a local database to show week-over-week trends (e.g., "You've been leaning into an external locus all week—let's examine why").
2. **Contextual Variables:** Add temporal awareness (e.g., different opening nodes for a Friday afternoon vs. a Monday evening).