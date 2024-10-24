import rclpy
from rclpy. node import Node
from std_srvs.srv import Trigger


class ServiceNode(Node):
    def __init__(self):
        super(ServiceNode, self).__init__('service_node')

        self.declare_parameter("service_name", "")
        self.declare_parameter("default_string", "")

        self.service_name = self.get_parameter("service_name").get_parameter_value().string_value
        self.default_string = self.get_parameter("default_string").get_parameter_value().string_value

        self.client = self.create_client(Trigger, "/spgc/trigger")

        self.store = ""
        self.service = self.create_service(Trigger, self.service_name, self.service_callback)

        if self.client.wait_for_service(timeout_sec=1.0):
            result = self.client.call_async(Trigger.Request())
            rclpy.spin_until_future_complete(self, result)
            self.store = result.result().message
        else:
            self.store = self.default_string

    def service_callback(self, request, response):
        response.message = self.store
        response.success = True
        return response


def main():
    rclpy.init()
    node = ServiceNode()

    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
