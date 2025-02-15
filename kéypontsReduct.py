def order_points_convex(points):
    """
    Orders the points to form a convex quadrilateral (rectangle).
    """
    if len(points) != 4:
        return points  # Only works for quadrilaterals
    
    # Calculate the centroid of the points
    centroid_x = sum(p[0] for p in points) / 4
    centroid_y = sum(p[1] for p in points) / 4
    
    # Sort points by angle relative to the centroid
    def angle_from_centroid(point):
        return math.atan2(point[1] - centroid_y, point[0] - centroid_x)
    
    sorted_points = sorted(points, key=angle_from_centroid)
    return sorted_points
    
def filter_images_with_4_plus_keypoints(directory):
    """
    Filters images that have polygons with more than 4 keypoints.
    Returns a list of file paths for such images.
    """
    json_files = [f for f in os.listdir(directory) if f.endswith(".json")]
    filtered_files = []

    for filename in json_files:
        json_path = os.path.join(directory, filename)
        with open(json_path, 'r') as f:
            keypoints = json.load(f)
        
        if "shapes" not in keypoints:
            continue
        
        for shape in keypoints["shapes"]:
            if len(shape["points"]) > 4:
                filtered_files.append(json_path)
                break  # Stop checking other shapes in the same file
    
    return filtered_files
    
def is_convex(points):
    """
    Checks if the given points form a convex polygon.
    """
    if len(points) < 3:
        return False  # A polygon must have at least 3 points
    
    polygon = Polygon(points)
    return polygon.is_valid and polygon.convex_hull.equals(polygon)
    
def ensure_rectangle_shape(points):
    """
    Ensures the points form a rectangle-shaped polygon.
    """
    if len(points) != 4:
        return points  # Only works for quadrilaterals
    
    # Order the points to form a convex quadrilateral
    ordered_points = order_points_convex(points)
    
    # Check if the ordered points form a convex polygon
    if is_convex(ordered_points):
        return ordered_points
    else:
        # If not convex, adjust the points slightly
        adjusted_points = [(x + 0.01 * i, y + 0.01 * i) for i, (x, y) in enumerate(ordered_points)]
        return adjusted_points


def find_closest_points(points):
    min_distance = float('inf')
    closest_pair = None
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if distance < min_distance:
                min_distance = distance
                closest_pair = (i, j)
    
    return closest_pair
    
def replace_closest_points(points):
    if len(points) > 4:
        # Find the two closest points
        i, j = find_closest_points(points)
        # Calculate the midpoint of the two closest points
        midpoint = (
            (points[i][0] + points[j][0]) / 2,
            (points[i][1] + points[j][1]) / 2
        )
        # Replace the two closest points with the midpoint
        new_points = [point for idx, point in enumerate(points) if idx not in (i, j)]
        new_points.append(midpoint)
        return new_points
    return points
def reorder_points(points):
    """
    Reorders the points to ensure:
    - x1: top-left
    - x2: top-right
    - x3: bottom-right
    - x4: bottom-left
    """
    if len(points) != 4:
        return points  # Only works for quadrilaterals
    
    # Sort points by y-coordinate (top to bottom)
    sorted_by_y = sorted(points, key=lambda p: p[1])
    
    # Separate top and bottom points
    top_points = sorted_by_y[:2]  # Top two points (smallest y)
    bottom_points = sorted_by_y[2:]  # Bottom two points (largest y)
    
    # Sort top points by x-coordinate (left to right)
    top_points_sorted = sorted(top_points, key=lambda p: p[0])
    x1 = top_points_sorted[0]  # Top-left
    x2 = top_points_sorted[1]  # Top-right
    
    # Sort bottom points by x-coordinate (left to right)
    bottom_points_sorted = sorted(bottom_points, key=lambda p: p[0])
    x4 = bottom_points_sorted[0]  # Bottom-left
    x3 = bottom_points_sorted[1]  # Bottom-right
    
    # Return reordered points
    return [x1, x2, x3, x4]
label_data = []
