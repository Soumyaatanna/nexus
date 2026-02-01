"""
Tests for Knowledge Graph Module
"""

import pytest
import tempfile
from pathlib import Path
from nexus.knowledge_graph import KnowledgeGraph, NodeType, RelationType


def test_knowledge_graph_creation():
    """Test creating a new knowledge graph"""
    kg = KnowledgeGraph(name="test_graph")
    assert kg.name == "test_graph"
    assert kg.graph.number_of_nodes() == 0
    assert kg.graph.number_of_edges() == 0


def test_add_node():
    """Test adding nodes to the graph"""
    kg = KnowledgeGraph(name="test")
    
    node_id = kg.add_node("test_func", NodeType.FUNCTION, {"name": "test_function"})
    assert node_id == "test_func"
    assert kg.graph.number_of_nodes() == 1
    
    node_data = kg.get_node("test_func")
    assert node_data is not None
    assert node_data['type'] == NodeType.FUNCTION.value
    assert node_data['name'] == "test_function"


def test_add_edge():
    """Test adding edges between nodes"""
    kg = KnowledgeGraph(name="test")
    
    kg.add_node("node1", NodeType.FUNCTION, {"name": "func1"})
    kg.add_node("node2", NodeType.FUNCTION, {"name": "func2"})
    
    edge = kg.add_edge("node1", "node2", RelationType.CALLS)
    assert edge == ("node1", "node2")
    assert kg.graph.number_of_edges() == 1


def test_get_neighbors():
    """Test getting neighboring nodes"""
    kg = KnowledgeGraph(name="test")
    
    kg.add_node("node1", NodeType.MODULE, {"name": "module1"})
    kg.add_node("node2", NodeType.FUNCTION, {"name": "func1"})
    kg.add_node("node3", NodeType.FUNCTION, {"name": "func2"})
    
    kg.add_edge("node1", "node2", RelationType.USES)
    kg.add_edge("node1", "node3", RelationType.USES)
    
    neighbors = kg.get_neighbors("node1")
    assert len(neighbors) == 2
    assert "node2" in neighbors
    assert "node3" in neighbors


def test_find_path():
    """Test finding paths between nodes"""
    kg = KnowledgeGraph(name="test")
    
    kg.add_node("a", NodeType.FUNCTION, {"name": "a"})
    kg.add_node("b", NodeType.FUNCTION, {"name": "b"})
    kg.add_node("c", NodeType.FUNCTION, {"name": "c"})
    
    kg.add_edge("a", "b", RelationType.CALLS)
    kg.add_edge("b", "c", RelationType.CALLS)
    
    path = kg.find_path("a", "c")
    assert path is not None
    assert path == ["a", "b", "c"]
    
    # Test no path
    kg.add_node("d", NodeType.FUNCTION, {"name": "d"})
    path = kg.find_path("a", "d")
    assert path is None


def test_search_nodes():
    """Test searching for nodes"""
    kg = KnowledgeGraph(name="test")
    
    kg.add_node("func1", NodeType.FUNCTION, {"name": "test_func", "module": "main"})
    kg.add_node("func2", NodeType.FUNCTION, {"name": "other_func", "module": "utils"})
    kg.add_node("class1", NodeType.CLASS, {"name": "TestClass", "module": "main"})
    
    # Search by type
    functions = kg.search_nodes(node_type=NodeType.FUNCTION)
    assert len(functions) == 2
    
    # Search by property
    main_nodes = kg.search_nodes(module="main")
    assert len(main_nodes) == 2


def test_get_statistics():
    """Test getting graph statistics"""
    kg = KnowledgeGraph(name="test")
    
    kg.add_node("node1", NodeType.FUNCTION, {"name": "func1"})
    kg.add_node("node2", NodeType.CLASS, {"name": "class1"})
    kg.add_edge("node1", "node2", RelationType.USES)
    
    stats = kg.get_statistics()
    assert stats['num_nodes'] == 2
    assert stats['num_edges'] == 1
    assert NodeType.FUNCTION.value in stats['node_types']
    assert NodeType.CLASS.value in stats['node_types']


def test_save_and_load():
    """Test saving and loading knowledge graphs"""
    kg = KnowledgeGraph(name="test_persistence")
    
    kg.add_node("node1", NodeType.FUNCTION, {"name": "func1"})
    kg.add_node("node2", NodeType.CLASS, {"name": "class1"})
    kg.add_edge("node1", "node2", RelationType.USES)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_graph.nexus"
        kg.save(filepath)
        
        # Load it back
        loaded_kg = KnowledgeGraph.load(filepath)
        
        assert loaded_kg.name == "test_persistence"
        assert loaded_kg.graph.number_of_nodes() == 2
        assert loaded_kg.graph.number_of_edges() == 1
        assert loaded_kg.get_node("node1") is not None


def test_get_connected_component():
    """Test getting connected components"""
    kg = KnowledgeGraph(name="test")
    
    # Create two separate components
    kg.add_node("a1", NodeType.FUNCTION, {"name": "a1"})
    kg.add_node("a2", NodeType.FUNCTION, {"name": "a2"})
    kg.add_edge("a1", "a2", RelationType.CALLS)
    
    kg.add_node("b1", NodeType.FUNCTION, {"name": "b1"})
    kg.add_node("b2", NodeType.FUNCTION, {"name": "b2"})
    kg.add_edge("b1", "b2", RelationType.CALLS)
    
    component_a = kg.get_connected_component("a1")
    assert len(component_a) == 2
    assert "a1" in component_a
    assert "a2" in component_a
    assert "b1" not in component_a
