import osmnx as ox
import networkx as nx

# Configure OSMnx
ox.config(use_cache=True, log_console=False)

# Cache graphs by region
_graph_cache = {}

def _get_graph_for_address(address: str):
    # Extract city/district name for graph bounding box
    # In a full app, parse address; here assume city is provided
    city = address.split(',')[-1].strip()
    if city not in _graph_cache:
        G = ox.graph_from_place(city, network_type='drive')
        _graph_cache[city] = G
    return _graph_cache[city]


def road_distance(addr1: str, addr2: str) -> float:
    """
    Returns the shortest road distance (in kilometers) between addr1 and addr2.
    """
    G1 = _get_graph_for_address(addr1)
    G2 = _get_graph_for_address(addr2)
    # Geocode points
    pt1 = ox.geocode(addr1)
    pt2 = ox.geocode(addr2)
    # Find nearest nodes
    u = ox.distance.nearest_nodes(G1, pt1[1], pt1[0])
    v = ox.distance.nearest_nodes(G2, pt2[1], pt2[0])
    # If graphs differ, merge or fallback to haversine
    if G1 is not G2:
        # Fallback: straight-line distance
        return ox.distance.great_circle_vec(pt1[0], pt1[1], pt2[0], pt2[1]) / 1000
    length = nx.shortest_path_length(G1, u, v, weight='length')
    return length / 1000  # meters to km
