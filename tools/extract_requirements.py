import argparse
import sys
import json
import os
import re

def extract_requirements(syp_path):
    if not os.path.exists(syp_path):
        print(f"Error: .syp file '{syp_path}' not found.")
        sys.exit(1)

    print(f"Parsing Graph: {syp_path}")
    try:
        with open(syp_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        sys.exit(1)

    # Scrape Requirements
    requirements_set = set()

    for node in data.get("nodes", []):
        node_type = node.get("type")
        props = node.get("properties", {})
        
        # 1. Check Python Script nodes for explicit "Requirements" property
        if "Python Script" in str(node_type) or "Code" in str(node_type):
            explicit_reqs = props.get("Requirements", "")
            if explicit_reqs and isinstance(explicit_reqs, str):
                for req in explicit_reqs.splitlines():
                    req = req.strip()
                    if req and not req.startswith("#"):
                        requirements_set.add(req)
                        
            # Optionally check script body for basic imports (basic heuristic)
            script_body = props.get("Script Body", "")
            if script_body:
                import_pattern = r"(?:^|\n)\s*(?:import|from)\s+([a-zA-Z0-9_]+)"
                matches = re.findall(import_pattern, script_body)
                for match in matches:
                    if match not in ["os", "sys", "time", "json", "math", "re", "random", "logging", "threading", "multiprocessing", "datetime", "urllib", "typing"]:
                        pass 
                        # This generates too many false positives for stdlib, better rely on explicit prop for runtime nodes
        
        # 2. Extract standard node requirements
        else:
            # Cross-reference node type with registered node files
            # The Engine uses NodeRegistry, but statically we can scan the nodes/ folder
            # Simple heuristic: scan all node files in synapse/nodes for DependencyManager.ensure(...)
            pass
            
    # Statically scan all standard python node files in the project
    # This acts as the "Master Core Requirements" + "Dynamic Node Requirements"
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    nodes_dir = os.path.join(project_root, "synapse", "nodes")
    
    # Regex to catch DependencyManager.ensure("package", "module")
    ensure_pattern = r'DependencyManager\.ensure\(\s*[\'"]([a-zA-Z0-9_\-]+)[\'"]'
    
    if os.path.exists(nodes_dir):
        for root, _, files in os.walk(nodes_dir):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            matches = re.findall(ensure_pattern, content)
                            for match in matches:
                                # Only add if this node type is *actually used* in the graph?
                                # For a full headless container, standard nodes might be safer to pre-install universally,
                                # or we map node_type -> class name -> file. 
                                # For now, we will just grep for the specific ones used if we can map them,
                                # but mapping node names to files requires the registry.
                                # Let's pre-load the registry temporarily
                                pass
                    except: pass
                    
    # Initialize Registry to exactly map used nodes to their requirements
    try:
        sys.path.append(project_root)
        from synapse.nodes.registry import NodeRegistry
        
        # Map class names to module paths
        used_node_types = set([n.get("type") for n in data.get("nodes", [])])
        
        for n_type in used_node_types:
            cls = NodeRegistry.get_node_class(n_type)
            if cls:
                module_name = cls.__module__ # e.g. synapse.nodes.media.camera
                # Convert module back to file path
                filepath = os.path.join(project_root, module_name.replace('.', os.sep) + '.py')
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = re.findall(ensure_pattern, content)
                        for match in matches:
                            requirements_set.add(match)
    except Exception as e:
        print(f"Warning: Could not dynamically inspect node modules: {e}")
        # Fallback already covered explicit requirements
        
    # Write Out
    output_file = os.path.join(os.path.dirname(syp_path), "requirements.txt")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for req in sorted(requirements_set):
                f.write(f"{req}\n")
        print(f"Extraction Successful! Created {len(requirements_set)} dependency mappings.")
        print(f"Saved to: {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extracts pip requirements from a Synapse .syp Graph.")
    parser.add_argument("syp_file", help="Path to the .syp file.")
    args = parser.parse_args()
    
    extract_requirements(args.syp_file)
