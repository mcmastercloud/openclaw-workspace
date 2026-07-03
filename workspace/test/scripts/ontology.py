import argparse
import json
import os
import sys

# Simplified Ontology CLI
# In a real scenario, this would use a proper DB; using a jsonl file as per instruction.

STORAGE_FILE = "memory/ontology/graph.jsonl"

def append_to_graph(entry):
    with open(STORAGE_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def create_entity(type, props):
    # Minimal ID generation for demo
    id = f"{type.lower()}_{os.urandom(2).hex()}"
    entity = {"id": id, "type": type, "properties": props, "relations": []}
    append_to_graph({"op": "create", "entity": entity})
    print(f"Created {type} with id: {id}")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--type", required=True)
    create_parser.add_argument("--props", required=True)
    
    args = parser.parse_args()
    
    if args.command == "create":
        props = json.loads(args.props)
        create_entity(args.type, props)

if __name__ == "__main__":
    main()
