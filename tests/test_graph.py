from engine.graph_builder import DocumentGraph

graph = DocumentGraph()

# Add relationships
graph.add_relation("Driving License", "Vehicle Registration")
graph.add_relation("Vehicle Registration", "Vehicle Insurance")
graph.add_relation("Vehicle Insurance", "Challan")

graph.add_relation("PAN Card", "ePAN")
graph.add_relation("ePAN", "Form 16")

graph.add_relation("APAAR ID", "Class X Marksheet")
graph.add_relation("Class X Marksheet", "Class XII Marksheet")
graph.add_relation("Class XII Marksheet", "Degree Certificate")

print("===== Graph Information =====")

print("\nNext after Driving License:")
print(graph.next_documents("Driving License"))

print("\nNext after PAN Card:")
print(graph.next_documents("PAN Card"))

print("\nPrevious of Vehicle Insurance:")
print(graph.previous_documents("Vehicle Insurance"))

print("\nPrevious of Degree Certificate:")
print(graph.previous_documents("Degree Certificate"))

print("\nTotal Documents:", graph.total_documents())
print("Total Relations:", graph.total_relations())

print("\n===== All Documents =====")
print(graph.get_all_documents())

print("\n===== All Relationships =====")
print(graph.get_all_relations())