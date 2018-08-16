@nrp.MapRobotPublisher("topic_finger1", Topic('/robot/finger1_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_finger2", Topic('/robot/finger2_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotSubscriber('command', Topic('/arm_robot/hand_commands', std_msgs.msg.String))
@nrp.MapVariable("last_command_executed", initial_value=None)
@nrp.Neuron2Robot()
def gripper_control(t, command, last_command_executed, topic_finger1, topic_finger2):

    if command.value is None:
        return
    else:
        command_str = command.value.data

    if command_str == last_command_executed.value:
        return

    clientLogger.info("Gripper received: {}".format(command_str))

    def open_gripper():
        topic_finger1.send_message(std_msgs.msg.Float64(0.01))
        topic_finger2.send_message(std_msgs.msg.Float64(-0.01))

    def close_gripper():
        topic_finger1.send_message(std_msgs.msg.Float64(-0.01))
        topic_finger2.send_message(std_msgs.msg.Float64(0.01))

    def parse_grasping_command(cmd):
        do_grasp = None
        if cmd == "GRASP":
            do_grasp = 1
        elif cmd == "RELEASE":
            do_grasp = 0
        return do_grasp
        
    grasp = parse_grasping_command(command_str)
    if grasp is not None:
        last_command_executed.value = command_str
        if grasp:
            close_gripper()
        else:
            open_gripper()
        
