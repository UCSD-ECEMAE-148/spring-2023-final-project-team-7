# team 7 project2

import cv2
import depthai as dai
import contextlib
import os
import time

from pathlib import Path
from sensor_msgs.msg import Image
from std_msgs.msg import Header, Float32 #, Bool
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
import math
import numpy as np

NODE_NAME = "camera_node"

DETECTION_TOPIC_NAME = "detection"

class MultiCamNode(Node):

    def __init__(self):
        super().__init__(NODE_NAME)
        self.device_info = dai.Device.getAllAvailableDevices()
        self.q_rgb_list = []
        self.num_devices = len(self.device_info)
        self.cam_publishers = []
        for i in range(self.num_devices):
             self.cam_publishers.append(self.create_publisher(Image, "camera/color/image_raw", 10))
        
        self.detection_publisher = self.create_publisher(Float32, DETECTION_TOPIC_NAME, 10) #self added, creating detection publisher
        self.bridge = CvBridge()
        

    #detection_publisher.publish(boolmsg) format for publisjing

    def getPipeline(self, preview_res = (300, 300)): #values were originally (1448,568)
        # import sys
        # Start defining a pipeline
        pipeline = dai.Pipeline()

        # Define a source - color camera
        cam_rgb = pipeline.create(dai.node.ColorCamera)
        # For the demo, just set a larger RGB preview size for OAK-D
        cam_rgb.setPreviewSize(preview_res[0], preview_res[1]) # FIX ME, need to match what ever pipeline we are using
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setInterleaved(False)

        ## define neural network type
        nn = pipeline.create(dai.node.MobileNetDetectionNetwork)

        ## define neural network path and parameters
        nn.setConfidenceThreshold(0.5)
        nn.setBlobPath(str((Path(__file__).parent / Path('/home/projects/ros2_ws/src/ucsd_robocar_hub2/ucsd_robocar_sensor2_pkg/mobilenet-ssd_openvino_2021.4_6shave.blob')).resolve().absolute()))
        nn.setNumInferenceThreads(2)
        nn.input.setBlocking(False)
        cam_rgb.preview.link(nn.input)
        nnOut = pipeline.create(dai.node.XLinkOut)
        nnOut.setStreamName("nn")
        nn.out.link(nnOut.input)

        self.labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

        # Create output
        xout_rgb = pipeline.create(dai.node.XLinkOut)
        xout_rgb.setStreamName("rgb")
        cam_rgb.preview.link(xout_rgb.input)

        monoLeft = pipeline.create(dai.node.MonoCamera)
        monoRight = pipeline.create(dai.node.MonoCamera)
        stereo = pipeline.create(dai.node.StereoDepth)
        spatialLocationCalculator = pipeline.create(dai.node.SpatialLocationCalculator)

        xoutDepth = pipeline.create(dai.node.XLinkOut)
        xoutSpatialData = pipeline.create(dai.node.XLinkOut)
        xinSpatialCalcConfig = pipeline.create(dai.node.XLinkIn)

        xoutDepth.setStreamName("depth")
        xoutSpatialData.setStreamName("spatialData")
        xinSpatialCalcConfig.setStreamName("spatialCalcConfig")

        # Properties for the depth measurement cameras
        monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

        stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        stereo.setLeftRightCheck(True)
        stereo.setExtendedDisparity(True)
        spatialLocationCalculator.inputConfig.setWaitForMessage(False)

        # Create 10 ROIs
        for i in range(10):
            config = dai.SpatialLocationCalculatorConfigData()
            config.depthThresholds.lowerThreshold = 200
            config.depthThresholds.upperThreshold = 10000
            config.roi = dai.Rect(dai.Point2f(i*0.1, 0.45), dai.Point2f((i+1)*0.1, 0.55))
            spatialLocationCalculator.initialConfig.addROI(config)

        # Linking for the depth measurements
        monoLeft.out.link(stereo.left)
        monoRight.out.link(stereo.right)

        spatialLocationCalculator.passthroughDepth.link(xoutDepth.input)
        stereo.depth.link(spatialLocationCalculator.inputDepth)

        spatialLocationCalculator.out.link(xoutSpatialData.input)
        xinSpatialCalcConfig.out.link(spatialLocationCalculator.inputConfig)

        return pipeline


    def camera_initialization(self, debug = False, path = "./"):

        # https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack
        with contextlib.ExitStack() as stack:
            device_infos = dai.Device.getAllAvailableDevices()
            if len(device_infos) == 0:
                raise RuntimeError("No devices found!")
            else:
                print("Found", len(device_infos), "devices")

            for device_info in device_infos:
                print(device_info)
                openvino_version = dai.OpenVINO.Version.VERSION_2021_4
                usb2_mode = False
                device = stack.enter_context(dai.Device(openvino_version, device_info, usb2_mode))

                # Note: currently on POE, DeviceInfo.getMxId() and Device.getMxId() are different!
                print("=== Connected to " + device_info.getMxId())
                mxid = device.getMxId()
                cameras = device.getConnectedCameras()
                usb_speed = device.getUsbSpeed()
                print("   >>> MXID:", mxid)
                print("   >>> Cameras:", *[c.name for c in cameras])
                print("   >>> USB speed:", usb_speed.name)


                # Get a customized pipeline based on identified device type
            
                pipeline = self.getPipeline()
                
                print("   >>> Loading pipeline for: OAK-D-LITE")
                device.startPipeline(pipeline)

                # Output queue will be used to get the rgb frames from the output defined above
                q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
                stream_name = "rgb-" + mxid + "-" + "OAK-D"
                self.q_rgb_list.append((q_rgb, stream_name))

                qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False) #getting output queue of NN

                #getting output queue of depth detection network
                depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False) #required
                spatialCalcQueue = device.getOutputQueue(name="spatialData", maxSize=4, blocking=False)

                detections = [] #defining array of detections


            if debug:
                    self.image_display_opencv(path = path)
                
            else:
                #start_time = time.time()
                while True:

                    # spatialData = spatialCalcQueue.get().getSpatialLocations()

                    # distanceArr = []
        
                    # for depthData in spatialData[2:8]:

                    #     coords = depthData.spatialCoordinates
                    #     distance = math.sqrt(coords.x ** 2 + coords.y ** 2 + coords.z ** 2)/1000
                    #     distanceArr.append(distance)
                    
                    
                    # minDist = np.min(distanceArr)

                    # print(len(distanceArr))


                    # print(np.min(distanceArr))


                    inDet = qDet.tryGet()
                    if inDet is not None:
                        spatialData = spatialCalcQueue.get().getSpatialLocations()

                        distanceArr = []
        
                        for depthData in spatialData[2:8]:

                            coords = depthData.spatialCoordinates
                            distance = math.sqrt(coords.x ** 2 + coords.y ** 2 + coords.z ** 2)/1000
                            distanceArr.append(distance)
                    
                        minDist = np.min(distanceArr)

                        detections = inDet.detections
                        detected = 1.0 # False
                        for detection in detections:
                            if self.labelMap[detection.label] == "person" or self.labelMap[detection.label] == "car":

                                print(self.labelMap[detection.label])
                                detected = round(minDist,1) # True                       
                        #bool_msg = Bool()
                        float_msg = Float32()
                        float_msg.data = detected 
                        print(float_msg.data)
                        self.detection_publisher.publish(float_msg)
                               

                    for i, (q_rgb, _) in enumerate(self.q_rgb_list):
                        in_rgb = q_rgb.tryGet()

                        if in_rgb is not None:
                            img_msg = self.bridge.cv2_to_imgmsg(in_rgb.getCvFrame(), "bgr8")
                            self.cam_publishers[i].publish(img_msg)
                            print("image2")

                    if cv2.waitKey(1) == ord('q'):
                        break

    
    def image_display_opencv(self, path): # debug purpose only
        img_cnt = 0
        while True:
            for q_rgb, stream_name in self.q_rgb_list:
                in_rgb = q_rgb.tryGet()
                if in_rgb is not None:
                    cv2.imshow(stream_name, in_rgb.getCvFrame())
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('s'):
                        cv2.imwrite(os.path.join(path, str(img_cnt) + '.bmp'), in_rgb.getCvFrame())
                        print("Saved image: ", img_cnt)
                        img_cnt += 1
                    elif key == ord('q'):
                        exit("user quit")



def main():

    rclpy.init()
    cam_node = MultiCamNode()
    try:
    	cam_node.camera_initialization(debug=False, path ='/home/projects/sensor2_ws/src/camera/oakd_debug/cv_img_save')
    except KeyboardInterrupt:
        print(f"\nShutting down {NODE_NAME}...")
        # Kill cv2 windows and node
        cv2.destroyAllWindows()
        cam_node.destroy_node()
        rclpy.shutdown()
        print(f"{NODE_NAME} shut down successfully.")


if __name__ == "main":
    main()
