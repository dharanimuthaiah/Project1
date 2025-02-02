def sysCall_init():
    sim = require('sim')

    self.bot_handle = sim.getObject('/body')
    if self.bot_handle == -1:
        print("Error: 'body' object not found.")
        return

    self.right_joint_handle = sim.getObject('/body/right_joint')
    self.left_joint_handle = sim.getObject('/body/left_joint')
    self.right_wheel_handle = sim.getObject('/body/right_joint/right_wheel')
    self.left_wheel_handle = sim.getObject('/body/left_joint/left_wheel')

    if any(h == -1 for h in [self.right_joint_handle, self.left_joint_handle,
                              self.right_wheel_handle, self.left_wheel_handle]):
        print("Error: One or more objects not found.")
        return
        
    self.joint_velocities = [0, 0]  
    self.gains = [0.70, 0.0]  
    self.tilt_angle = 0  
    self.yaw_rate = 0  
def sysCall_actuation():
    sim = require('sim')
    sim.setJointTargetVelocity(self.right_joint_handle, self.joint_velocities[1])
    sim.setJointTargetVelocity(self.left_joint_handle, self.joint_velocities[0])

def sysCall_sensing():
    sim = require('sim')
    message, data, _ = sim.getSimulatorMessage()
    
    if message == sim.message_keypress:
        if data[0] == 2007: 
            self.joint_velocities = [5,5]  
            self.yaw_rate = 0
            print("Input 2007: Moving forward")
        elif data[0] == 2008: 
            self.joint_velocities = [-4, -4] 
            self.yaw_rate = 0
            print("Input 2008: Moving backward")
        elif data[0] == 2009:  
            self.joint_velocities = [2,-2] 
            self.yaw_rate = 1
            print("Input 2009: Turning left")
        elif data[0] == 2010:  
            self.joint_velocities = [-2,2] 
            self.yaw_rate = -1
            print("Input 2010: Turning right")
        elif data[0] == 88:  
            self.joint_velocities = [0, 0]  
            self.yaw_rate = 0
            print("Input 88: Stopping")
        else: 
            print("No valid input:self.joint_velocities = [0, 0] ")

    

def sysCall_cleanup():
    pass
