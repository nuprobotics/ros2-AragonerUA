import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Receiver(Node):
    def __init__(self):
        super().__init__('receiver')
        # Subscribe to /spgc/sender topic
        self.subscription = self.create_subscription(
            String,
            '/spgc/sender',
            self.listener_callback,
            10
        )
        self.subscription  # To prevent the variable from being garbage collected

    def listener_callback(self, msg):
        # Log the received message at INFO level
        self.get_logger().info(f'Received message: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = Receiver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()