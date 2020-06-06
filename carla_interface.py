import sys
import glob
import os
import PARAMETERS as PM
import numpy as np

class Carla:

    def __init__(self):

        sys.path.insert(1, 'D:/Data/GitHub_Repos/carla_dist/WindowsNoEditor/PythonAPI/examples')
        try:
            sys.path.append(glob.glob
                                (
                                'D:/Data/GitHub_Repos/carla_dist/WindowsNoEditor/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
                                    sys.version_info.major,
                                    sys.version_info.minor, 'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
        except IndexError:
            pass

        import carla

        self.actor_list = []

        client = carla.Client('127.0.0.1', 2000)
        client.set_timeout(2.0)
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()

        # *************************************** Add Vehicle ****************************************
        bp = blueprint_library.filter("audi")[2]
        spawn_point = world.get_map().get_spawn_points()[30]
        vehicle = world.spawn_actor(bp, spawn_point)
        vehicle.set_autopilot(True)
        # vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
        self.actor_list.append(vehicle)

        # *************************************** Add Cameras ****************************************
        cam_bp = blueprint_library.find("sensor.camera.rgb")
        cam_bp.set_attribute('image_size_x', f'{PM.RESIZED_FRAME_SIZE[0]}')
        cam_bp.set_attribute('image_size_y', f'{PM.RESIZED_FRAME_SIZE[1]}')
        cam_bp.set_attribute('fov', '50')

        spawn_point = carla.Transform(carla.Location(x=0.4, y=-0.5, z=1.5))
        self.camera_left = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)
        self.actor_list.append(self.camera_left)
        spawn_point = carla.Transform(carla.Location(x=0.4, y=0.5, z=1.5))
        self.camera_right = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)
        self.actor_list.append(self.camera_right)

        self.camera_left.listen(lambda data: self.get_image(data, 'left'))
        self.camera_right.listen(lambda data: self.get_image(data, 'right'))

        self.left_image = ()
        self.right_image = ()

    def get_image(self, image, camera):
        img = np.array(image.raw_data)
        img2 = img.reshape((PM.RESIZED_FRAME_SIZE[1], PM.RESIZED_FRAME_SIZE[0], 4))
        img3 = img2[:, :, :3]
        if camera == 'left':
            self.left_image = img3
        if camera == 'right':
            self.right_image = img3

    def destroy(self):
        for actor in self.actor_list:
            actor.destroy()
        print("All cleaned up!")
