import os
import re
import sys

def get_mermaid_mindmap(root_dir):
    nodes = set()
    edges = set()
    
    # regex for [[link]] or [text](file.md)
    link_pattern = re.compile(r'\[\[(.*?)\]\]|\[.*?\]\((.*?\.md)\)')

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                filepath = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(filepath, root_dir)
                source_node = rel_path
                nodes.add(source_node)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = link_pattern.findall(content)
                    for wiki_link, md_link in matches:
                        target_node = wiki_link if wiki_link else md_link
                        # normalize target_node
                        if not target_node.endswith('.md'):
                            target_node += '.md'
                        
                        # clean target_node path if it's relative
                        # this is a simple mapper, so we'll just use the base name for target
                        target_node = os.path.basename(target_node)
                        edges.add((source_node, target_node))

    if not nodes:
        return "graph TD\n  Empty[No Markdown files found]"

    mermaid_lines = ["graph TD"]
    for source, target in edges:
        # Mermaid node names can't have certain characters
        s = source.replace(' ', '_').replace('.', '_').replace('/', '_')
        t = target.replace(' ', '_').replace('.', '_').replace('/', '_')
        mermaid_lines.append(f'  {s}["{source}"] --> {t}["{target}"]')
    
    # ensure nodes with no edges are still shown
    all_edge_nodes = set([s for s, t in edges] + [t for s, t in edges])
    for node in nodes:
        if node not in all_edge_nodes:
            n = node.replace(' ', '_').replace('.', '_').replace('/', '_')
            mermaid_lines.append(f'  {n}["{node}"]')

    return "\n".join(mermaid_lines)

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "projects"
    print(get_mermaid_mindmap(target_dir))
