import copy 
class Graph2Node:
    def __init__(self,name,edges={}):
        self.name = name
        self.edges = edges

class Graph2:
    def __init__(self,graph_arr):
        self.graph_arr = graph_arr
        self.graph_name_arr = []
        for item in graph_arr:
            self.graph_name_arr.append(item.name)

    def mst(self):
        explored_nodes=[0]
        unexplored_nodes = copy.deepcopy(self.graph_arr)
        mst = []
        i = 0
        temp_arr = []
        temp_edge_arr = []
        for every_node_index in explored_nodes:
            all_edges_for_node = unexplored_nodes[every_node_index].edges
            """
            Creating a minimum edge for the MST
            """
            min_node_name = min(all_edges_for_node, key=all_edges_for_node.get)
            name_corrosponding_node = unexplored_nodes[every_node_index].name
            min_edge = [name_corrosponding_node, min_node_name, all_edges_for_node[min_node_name]]
            temp_arr.append(all_edges_for_node[min_node_name])
            temp_edge_arr.append(min_edge)
        #removing newly explored edges from unexplored Array
        index_minimum_node_in_explored_nodes = temp_arr.index(min(temp_arr))
        new_node_name = temp_edge_arr[index_minimum_node_in_explored_nodes][1]
        corrosponding_node_name = temp_edge_arr[index_minimum_node_in_explored_nodes][0]
        unexplored_nodes[explored_nodes[index_minimum_node_in_explored_nodes]].edges.pop(new_node_name)
        index_corrosponding_node = self.graph_name_arr.index(temp_edge_arr[index_minimum_node_in_explored_nodes][1])
        unexplored_nodes[index_corrosponding_node].edges.pop(corrosponding_node_name)
        # mst.append(temp_edge_arr[index_minimum_node_in_explored_nodes])
        #Testing
        print(unexplored_nodes[0].edges)
        print(unexplored_nodes[1].edges)
        """
        ToDo
        Add explored node in explored nodes array
        Loop Through all the graph
        Generate Graph function
        """

        #unexplored_nodes[explored_nodes[index_minimum_node_in_explored_nodes]].edges.pop(temp_edge_arr[1]) #removing the min edge from first node


        # explored_nodes.append(self.graph_name_arr.index(min_node_name))
        # i += 1



first_node = Graph2Node("a",{"b":7,"c":3})
second_node = Graph2Node("b",{"a":7,"c":1})
third_node = Graph2Node("c",{"b":1,"a":3})

new_graph = Graph2([first_node,second_node,third_node])
new_graph.mst()


