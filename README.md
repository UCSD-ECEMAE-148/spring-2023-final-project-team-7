![Home | Jacobs School of Engineering](https://jacobsschool.ucsd.edu/sites/default/files/UCSDLogo_JSOE_BlueGold_0_0.png)

# **MAE 148 SPRING 2023: Team 7**
**Team Members:** (Left to Right) Qiudi He, William Zhao ,Blake Iwaisako, Jeffrey Han

<br />
<div align="center">
    <h3>Team 7 Members</h3>
    <p>
    </p>
</div>

<div align="center">
    <img src="Images\stone_cold.png" width="500" height="325">
</div>
<br>
<hr>
  



## Final Project: Pedestrian Detection/Avoidance



![](https://lh4.googleusercontent.com/7-Lq0UwWIEiCCS1BK4yUAiYpdFAxF_jG3UWVmiCunM1wiYCF471jUJyWZsKAK7qwSb9IPbliTvdOhNu2w2CW99g0bLbpQBlGtnhf7fxSZyWykeyOXdlGeBt9mdtzaq5NtX5m9G9W8erBSKHDkO7ciHw)

**Overview:** Develop an autonomous car that is capable of detecting and avoiding pedestrian-shaped obstacles while following a predetermined track. The OAKD camera will detect and analyze the environment, including the presence of pedestrians, and use that information to make decisions on how to maneuver around them. We will create a SEPARATE "pedestrian" car that will cross the road. 
## [--->Demonstration Video<---](https://youtube.com/shorts/CGoW5MynGYg)

### **Goals we Promised**

*Pedestrian Detection*
-   Detection Consistency
    
-   Distance Recognition
    
-   Pedestrian Movement (Car understands that it might collide with the pedestrian)

*Pedestrian Physical Movement*
-   Ensure “Legs” move in a straight line across the lane
    
-   Calibrate the speed “Legs” move
    
-   Pedestrian size (can it be detected?)
    

 *Pedestrian Avoidance*
    

-   Car waits for pedestrian to cross the road
    
-   Car stops a set distance away from pedestrian
    
-   Car moves backwards if pedestrian is too close
    

**Goals that would be nice to have**

-   Implement Lidar detection as a redundancy alongside the OAK-D camera


### Our Car
<div align="center">
    <img src="Images\robot_front" width="500" height="700">
    <img src="Images\robot_rear" width="500" height="700">
</div>

### Schematic

![](https://lh6.googleusercontent.com/lHdGcGr-w7B0qaoOZ7-al9tBV5ciCrxkm4RjfRRaDDolsIpb0sDMPScZsMEPxJio3CC6rlTdplljKFdJY-V1BhAphjcxq67uH3WXZJuXU8ZtW3aV5wbC7ufw3cEt9Wd8qY0UD_WeYtd6OGvudenjM1Y)

  

### Our Pedestrian Cutout
<div align="center">
    <img src="Images\pedestrian_cutout" width="500" height="700">
     <img src="Images\pedestrian car" width="500" height="700">
</div>

### Detection of the pedestrian cutout

![](https://lh6.googleusercontent.com/HwaLVYWWFR1nt4DSfjNUzTtaECIP2HjjGT86uvrPO-kEEY9Grtu53ja9n7r66BKhBDDcaSqEPdoQ2p8Irte1HIR07JTh67hM9frpC1oWc6o2Q2GjEfqVY_9H_Cw7PRzePl56N9CGAs_uKrH62LEJ0f0)

### Description of the Pedestrian “Legs”
The pedestrian's "legs" are made from an Arduino rover that utilizes an Adafruit motor shield. These motors are calibrated to move in a straight line prependicular to the predetermined path of the car.

<div align="center">
    <img src="Images\pedestrian_legs.gif" width="500" height="750">
</div>


### What We Used

-   ROS2 Framework
    
-   Built-in OAK-D depthai functions
    

### Initial Issues with recognition

When the pedestrian is attached to its “Legs” the OAK-D camera will often recognize it as a car instead of a person. Our solution is to tell the OAK-D to recognize both vehicles and humans as both “pedestrians”

<div align="center">
    <img src="Images\pedestrian_detect_1" width="200" height="200">
    <img src="Images\pedestrian_detect_2" width="200" height="200">
    <img src="Images\pedestrian_detect_3" width="200" height="200">
</div>

### What did not work as expected

-   Initially, the detection didn’t work well on moving targets. It would capture a person/car for a second, but then it would stop seeing it the next. This caused the stop and drive commands to interfere with each other.
    

-   Solution: Whenever the car detects a person, set a timer to hold that detection for a set amount of time. This would make it so that the car would stop for a set amount of time. This prevented it from being stuck in a cycle of stopping. (Completed)
    

-   Yellow Pedestrian: The model pedestrian had quite a bit of yellow on it. This would cause the car to follow it like a yellow line sometimes rather than stopping.
<div align="center">
    <img src="Images\pedestrian_painted" width="500" height="700">
</div>

-   Solution: Painted all yellow parts on the pedestrian black.
    

-   Potentially inconsistent depth recognition: The depth detection assumed that the closest object would always be the pedestrian. However, if it sees a person/car in the distance and also has something else close to it, it will stop at an unintended
    

### Accomplishments
Pedestrian Detection
    

-   OAK-D detection of the pedestrian works consistently, notices when the pedestrian crosses into its lane, and stops a safe distance away from the pedestrian.
    

Pedestrian Physical Movement
    

-   Our pedestrian car model is able to cross the road in a straight line and its shape can detected by the OAK-D camera.
    

Pedestrian Avoidance
    

-   Car is able to stop when it sees the pedestrian in its line of sight and back up. When pedestrian cross out of its view, across the road, the car proceeds forward.

### Tasks we could accomplish if we had more time...
- Track the pedestrian specifically to avoid detecting other objects

- Implement Lidar as a redundancy
    - This is helpful in case the pedestrian has any yellow colors on it

- Design the car to slow down as it nears the pedestrian to simulate a real life situation (It’s also healthier for the gearbox)

- Add a speaker with car horn audio if pedestrian stays in front of it for too long
    - Move around the pedestrian if it stays for too long



<div align="center">
    <h2>Early Quarter</h2>
</div>

## Links to Progress Videos
[First Autonomous Lap using GPS](https://www.youtube.com/watch?v=hCbwt8EDgjE)

[First Three Autonomous Laps using the OAK-D camera](https://www.youtube.com/watch?v=gDzq0wEswKs&t)  

[Yellow Line Following](https://www.youtube.com/watch?v=mlyeFP09i_I) 

[Inner Lane Following](https://www.youtube.com/watch?v=i9f_KKLGM4M)

## Custom Designed Hardware
### Camera Stand
<div align="center">
    <img src="Images\cam_assem.png" width="300" height="300">
    <img src="Images\cam_side.png" width="300" height="300">
</div>

### Magnetic Hinge Mounting Plate
<div align="center">
    <img src="Images\plate_assem.png" width="300" height="300">
</div>
