class Ant:
    def __init__(self, start_node):
        self.start_node = start_node
        self.current_node = start_node
        self.visited = [start_node]
        self.tour_length = 0.0

    def visit(self, node, distance):
        """Mrav posjećuje novi čvor i ažurira dužinu ture."""
        self.visited.append(node)
        self.tour_length += distance
        self.current_node = node

    def has_visited(self, node):
        return node in self.visited

    def tour_complete(self, total_nodes):
        return len(self.visited) == total_nodes

    def reset(self):
        self.visited = [self.start_node]
        self.current_node = self.start_node
        self.tour_length = 0.0