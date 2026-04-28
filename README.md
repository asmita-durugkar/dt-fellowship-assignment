# DeepThought Fellowship: Deterministic Reflection Agent

## Overview
This repository contains a deterministic, data-driven reflection agent. It enforces structured end-of-day reflection across three psychological axes (Locus, Orientation, Radius) without the use of an LLM at runtime, ensuring auditable, safe, and consistent user journeys.

## Repository Structure
* `/tree/reflection-tree.tsv` - The raw data structure of the reflection tree.
* `/tree/tree-diagram.png` - Visual map of the convergent-divergent node flow.
* `/agent/main.py` - The deterministic Python engine that executes the tree.
* `/agent/validator.py` - A structural audit script to ensure 100% path integrity.
* `/transcripts/` - Sample CLI outputs showing two opposing user journeys.
* `write-up.md` - Design rationale and psychological grounding.

## How to Run the Agent
1. Navigate to the directory containing the files (ensure `reflection-tree.tsv` is in the same directory as the script).
2. Run the interactive session via your terminal:
   ```bash
   python main.py