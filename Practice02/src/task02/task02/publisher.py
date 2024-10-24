import rclpy
import sys
from rclpy.node import Node
from std_msgs.msg import String

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher')

        # Declare parameters
        self.declare_parameter('text', 'Hello, ROS2!')
        self.declare_parameter('topic_name', '/spgc/receiver')

        # Get parameters from the config or command line
        self.text = self.get_parameter('text').get_parameter_value().string_value
        topic_name = self.get_parameter('topic_name').get_parameter_value().string_value

        # Create a publisher
        self.publisher_ = self.create_publisher(String, topic_name, 10)

        # Set a timer to periodically publish the message
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        msg = String()
        msg.data = self.text
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published message: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
