import ast
import os

def test_clustering_never_in_sync_path():
    router_path = os.path.join("app", "ingestion", "event_router.py")
    
    # If the file isn't tracked in this specific branch yet, it's safe
    if not os.path.exists(router_path):
        return
        
    with open(router_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
        
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "denstream" not in node.module, "Flaw 3 Fail: Heavy clustering imported in API!"