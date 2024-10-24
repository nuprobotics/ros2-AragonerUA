import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from rclpy.exceptions import ServiceUnavailableError

class ServiceNode(Node):
    def __init__(self):
        super().__init__('service_node')

        self.declare_parameter('service_name', '/trigger_service')
        self.declare_parameter('default_string', 'No service available')

        self.service_name = self.get_parameter('service_name').get_parameter_value().string_value
        self.default_string = self.get_parameter('default_string').get_parameter_value().string_value
        self.stored_value = self.default_string

        self.client = self.create_client(Trigger, '/spgc/trigger')
        self.call_trigger_service()

        self.create_service(Trigger, self.service_name, self.handle_service_request)

    def call_trigger_service(self):
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().warning("Service /spgc/trigger not available, using default value.")
            self.stored_value = self.default_string
        else:
            req = Trigger.Request()
            future = self.client.call_async(req)
            future.add_done_callback(self.trigger_callback)

    def trigger_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.stored_value = response.message
                self.get_logger().info(f"Stored value from /spgc/trigger: {self.stored_value}")
            else:
                self.get_logger().warning("Service /spgc/trigger returned unsuccessful response.")
                self.stored_value = self.default_string
        except (ServiceUnavailableError, Exception) as e:
            self.get_logger().error(f"Failed to call /spgc/trigger: {e}")
            self.stored_value = self.default_string

    def handle_service_request(self, request, response):
        response.success = True
        response.message = self.stored_value
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ServiceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
