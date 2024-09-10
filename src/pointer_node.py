import rclpy
from rclpy.node import Node
from franka_learning_msgs.srv import StringCmd
import evdev

class ReadPointerInputNode(Node):

    def __init__(self):
        super().__init__('pointer_node')  # Replace 'default' with a unique name

        # Retrieve parameters
        self.device_path = "/dev/input/event18"
        self.device_name = "Wireless Present Wireless Present Keyboard"

        self.control_client = self.create_client(StringCmd, "/learning_manager")

        self.start_loop()

    def exec_cmd(self, cmd):
        msg = StringCmd.Request()
        msg.cmd = cmd
        self.control_client.call_async(msg)

    def start_loop(self):
        if (self.device_path == "" or self.device_path == None):
            # Find device
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            self.get_logger().info(f"Looking for device name: {self.device_name}")
            for device in devices:
                if device.name == self.device_name:
                    self.device_path = device.path
                    self.get_logger().info(f"Choosing event device: {self.device_path}")
                    break

        # Open device
        try:
            self.dev = evdev.InputDevice(self.device_path)
        except Exception as e:
            self.get_logger().error(f"Could not find device: {e}")
            return

        while rclpy.ok():
            # Grab device context
            with self.dev.grab_context():
                grasp_release_counter = 0
                for event in self.dev.read_loop():
                    if event.code == evdev.ecodes.KEY_PAGEDOWN and event.value == 1:
                        if grasp_release_counter%2 == 0:
                            print("Grasp")
                            self.exec_cmd("grasp")
                        else:
                            print("Release")
                            self.exec_cmd("release")
                        grasp_release_counter += 1
                    elif event.code == evdev.ecodes.KEY_PAGEUP and event.value == 1:
                        print ("record")
                        self.exec_cmd("record")
                    elif (event.code == evdev.ecodes.KEY_ESC and event.value == 1) or (event.code == evdev.ecodes.KEY_F5 and event.value == 1):
                        print("REPLAY")
                        self.exec_cmd("replay")
                    elif event.code == evdev.ecodes.KEY_B and event.value == 1:
                        print("STOP")
                        self.exec_cmd("stop")
                        grasp_release_counter = 0

def main(args=None):
    rclpy.init(args=args)
    node = ReadPointerInputNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()