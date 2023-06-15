![Home | Jacobs School of Engineering](https://jacobsschool.ucsd.edu/sites/default/files/UCSDLogo_JSOE_BlueGold_0_0.png)

# **MAE 148 SPRING 2023: Team 7**
**Team Members:** Blake Iwaisako, William Zhao, Qiudi He, Jeffrey Han

<br />
<div align="center">
    <h3>ECE-MAE 148 Final Project</h3>
    <p>
    Team 3 Spring 2023
    </p>
</div>

<div align="center">
    <img src="Images\robot_front" width="500" height="700">
</div>
<br>
<hr>
  



## Final Project: Pedestrian Detection/Avoidance



![](https://lh4.googleusercontent.com/7-Lq0UwWIEiCCS1BK4yUAiYpdFAxF_jG3UWVmiCunM1wiYCF471jUJyWZsKAK7qwSb9IPbliTvdOhNu2w2CW99g0bLbpQBlGtnhf7fxSZyWykeyOXdlGeBt9mdtzaq5NtX5m9G9W8erBSKHDkO7ciHw)

**Overview:** Develop an autonomous car that is capable of detecting and avoiding pedestrian-shaped obstacles while following a predetermined track. The OAKD camera will detect and analyze the environment, including the presence of pedestrians, and use that information to make decisions on how to maneuver around them.

**Goals we Promised**

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
    <img src="Images\robot_" width="500" height="700">
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

### What We Used

-   ROS2 Framework
    
-   Built-in OAK-D depthai functions
    

### Initial Issues with recognition

When the pedestrian is attached to its “Legs” the OAK-D camera will often recognize it as a car instead of a person. Our solution is to tell the OAK-D to recognize both vehicles and humans as both “pedestrians”

![](https://lh3.googleusercontent.com/QTZ4NCvxMmY_l51k1HuYB_Uz7EuFox7yRXnJ7vJcom-xDKx-IzfFGIJVOH9cOAOFk8RbrbV2A_EcypMFleCnV9M6Igl9Y8GPbx-4VTBNMQ20kF1Mi_lIc4497er8jz-cQTAft5uk6wqWuSIKxsQeHy4)![](https://lh3.googleusercontent.com/14FT6iDPITJ5sfr040_L8rnILjH9nJC4gsGPc79_6a47BETYlT18mTcjJuaypcIrpNnLgKBYAWAqkt5tija1QQFdOkZKm1kZCG7VUwxoMpVxHfdJS7k1KKjYWV0GI1pCfuSAwkhfUV9mZHuXLzkMo_8)![](https://lh4.googleusercontent.com/ayKa_Bf2wtQDc7UIN0wOxV5nlxN-9MeW0vxH4tylaz9MPk312pY1pM17oDUCyoyHt3kOFoS8S5VD_mDtrtLZdiGwz3NsA-OuYP8Sbqp6eHvADzVQaZI0mIhWyB_qq6ZVNqF6RzwNqFWCcNC_0Owlt1k)

### What did not work as expected

-   Initially, the detection didn’t work well on moving targets. It would capture a person/car for a second, but then it would stop seeing it the next. This caused the stop and drive commands to interfere with each other.
    

-   Solution: Whenever the car detects a person, set a timer to hold that detection for a set amount of time. This would make it so that the car would stop for a set amount of time. This prevented it from being stuck in a cycle of stopping. (Completed)
    

-   Yellow Pedestrian: The model pedestrian had quite a bit of yellow on it. This would cause the car to follow it like a yellow line sometimes rather than stopping.
    

-   Solution: Painted all yellow parts on the pedestrian black. (Completed)
    

-   Potentially inconsistent depth recognition: The depth detection assumed that the closest object would always be the pedestrian. However, if it sees a person/car in the distance and also has something else close to it, it will stop at an unintended
    

### Accomplishments
Pedestrian Detection
    

-   OAK-D detection of the pedestrian works consistently, notices when the pedestrian crosses into its lane, and stops a safe distance away from the pedestrian.
    

Pedestrian Physical Movement
    

-   Our pedestrian car model is able to cross the road in a straight line and its shape can detected by the OAK-D camera.
    

Pedestrian Avoidance
    

-   Car is able to stop when it sees the pedestrian in its line of sight and back up. When pedestrian cross out of its view, across the road, the car proceeds forward.
    

## Early Quarter

### Links to Progress Videos
[First Autonomous Lap using GPS](https://www.youtube.com/watch?v=hCbwt8EDgjE)

[First Three Autonomous Laps using the OAK-D camera](https://www.youtube.com/watch?v=gDzq0wEswKs&t)  

[Yellow Line Following](https://www.youtube.com/watch?v=mlyeFP09i_I) 

[Inner Lane Following](https://www.youtube.com/watch?v=i9f_KKLGM4M)
