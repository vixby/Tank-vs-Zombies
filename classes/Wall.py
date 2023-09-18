from OpenGL.GL import *
from OpenGL.GLU import *
from classes.Shared import Vector
from scipy.spatial.distance import euclidean


class Wall:
    def __init__(self, corner_one, corner_two, corner_three, corner_four, corner_five):
        self.corners = [corner_one, corner_two,
                        corner_three, corner_four, corner_five]

        self.min_x = min(x for x, y in self.corners)
        self.max_x = max(x for x, y in self.corners)
        self.min_y = min(y for x, y in self.corners)
        self.max_y = max(y for x, y in self.corners)

    def draw(self):
        glPushMatrix()
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_TRIANGLE_FAN)
        for x, y in self.corners:
            glVertex2f(x, y)
        glEnd()
        glPopMatrix()

    def check_collision(self, x, y):
        return self.is_point_inside_wall((x, y))

    def is_point_inside_bounding_box(self, x, y):
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def is_point_inside_wall(self, point):
        x, y = point
        is_inside = False
        first_x, first_y = self.corners[0]
        # Loop through each edge of the polygon
        for i in range(1, len(self.corners) + 1):
            second_x, second_y = self.corners[i % len(self.corners)]
            if y > min(first_y, second_y):
                if y <= max(first_y, second_y):
                    # Check if point is to the left of the edge
                    if x <= max(first_x, second_x):
                        # Calculate x-intersect of the edge and the horizontal line through the point
                        if first_y != second_y:
                            x_intersect = (
                                y - first_y) * (second_x - first_x) / (second_y - first_y) + first_x
                        if first_x == second_x or x <= x_intersect:
                            is_inside = not is_inside
            first_x, first_y = second_x, second_y
        return is_inside

    def calculate_wall_normal(self, point1, point2):
        # Calculate wall_vector
        wall_vector = Vector(point2[0] - point1[0], point2[1] - point1[1])

        # Calculate normal by rotating wall_vector 90 degrees
        wall_normal = Vector(-wall_vector.y, wall_vector.x)

        length = (wall_normal.x ** 2 + wall_normal.y ** 2) ** 0.5
        wall_normal = Vector(wall_normal.x / length, wall_normal.y / length)
        return wall_normal

    def get_wall_points(self, projectile):
        min_distance = float("inf")
        closest_segment = None

        for i in range(len(self.corners)):
            point1 = self.corners[i]
            point2 = self.corners[(i + 1) % len(self.corners)]

            # Compute the distance from the projectile to this line segment
            distance = self.distance_from_point_to_line_segment(
                (projectile.position.x, projectile.position.y), point1, point2)

            # Update the closest segment if this one is closer
            if distance < min_distance:
                min_distance = distance
                closest_segment = (point1, point2)

        return closest_segment

    def distance_from_point_to_line_segment(self, point, point1, point2):
        line_vector = Vector(point2[0] - point1[0], point2[1] - point1[1])
        point_vector = Vector(point[0] - point1[0], point[1] - point1[1])
        dot_product = line_vector.dot(line_vector)

        if dot_product == 0:
            return euclidean(point, point1)

        t = max(0, min(1, point_vector.dot(line_vector) / dot_product))

        projection = (point1[0] + t * line_vector.x,
                      point1[1] + t * line_vector.y)

        return euclidean(point, projection)
