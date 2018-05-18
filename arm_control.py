# Imported Python Transfer Function
import numpy as np

# APPROACH
approach_tray_conf = np.array([0.0, 0.3, -1.0, 0.0, 0.0, 0.0])

# GRASP
grasp_conf_0 = np.array([0.6, 0.5, -2.4, 0.0, 0.0, 0.0])
grasp_conf_1 = np.array([0.4, 0.4, -2.2, 0.0, -0.3, 1.0])
grasp_conf_2 = np.array([0.3, 0.4, -1.6, 1.0, 0.0, 0.0])
grasp_conf_3 = np.array([-0.15, 0.4, -1.8, -0.2, 0.0, 0.2])
grasp_conf_4 = np.array([0.3, 0.4, -2.2, 0.0, -0.3, 0.5])
grasp_conf_5 = np.array([0.0, 0.4, -2.0, 0.3, 0.3, 0.0])
grasp_conf_6 = np.array([0.6, 0.4, -2.0, 1.0, 0.0, 0.7])
grasp_conf_7 = np.array([0.0, 0.4, -2.4, 0.4, 0.5, 0.0])
grasp_conf_8 = np.array([0.3, 0.5, -2.0, 0.6, -0.5, 0.0])
grasp_conf_9 = np.array([0.8, 0.1, -2.5, 0.7, 0.0, 1.0])

# DISPOSE
dispose_tray_conf = np.array([-0.7, -0.3, -2.0, 0.0, 0.0, 0.0])

# RESET
reset_conf = np.zeros(6)

@nrp.MapRobotPublisher("topic_arm_1", Topic('/robot/hollie_000_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_2", Topic('/robot/hollie_001_base_x_rot_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_3", Topic('/robot/hollie_002_upper_x_rot_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_4", Topic('/robot/hollie_003_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_5", Topic('/robot/hollie_004_wrist_x_rot_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_6", Topic('/robot/hollie_005_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotSubscriber('command', Topic('/arm_robot/arm_commands', std_msgs.msg.String))
@nrp.MapVariable("last_command_executed", initial_value=None)
@nrp.MapVariable("approach_tray_conf", initial_value=approach_tray_conf)
@nrp.MapVariable("grasp_conf_0", initial_value=grasp_conf_0)
@nrp.MapVariable("grasp_conf_1", initial_value=grasp_conf_1)
@nrp.MapVariable("grasp_conf_2", initial_value=grasp_conf_2)
@nrp.MapVariable("grasp_conf_3", initial_value=grasp_conf_3)
@nrp.MapVariable("grasp_conf_4", initial_value=grasp_conf_4)
@nrp.MapVariable("grasp_conf_5", initial_value=grasp_conf_5)
@nrp.MapVariable("grasp_conf_6", initial_value=grasp_conf_6)
@nrp.MapVariable("grasp_conf_7", initial_value=grasp_conf_7)
@nrp.MapVariable("grasp_conf_8", initial_value=grasp_conf_8)
@nrp.MapVariable("grasp_conf_9", initial_value=grasp_conf_9)
@nrp.MapVariable("dispose_tray_conf", initial_value=dispose_tray_conf)
@nrp.MapVariable("reset_conf", initial_value=reset_conf)
@nrp.Neuron2Robot()
def arm_control(t, command, last_command_executed, approach_tray_conf,
                grasp_conf_0, grasp_conf_1, grasp_conf_2, grasp_conf_3, grasp_conf_4,
                grasp_conf_5, grasp_conf_6, grasp_conf_7, grasp_conf_8, grasp_conf_9,
                dispose_tray_conf, reset_conf, topic_arm_1, topic_arm_2, topic_arm_3,
                topic_arm_4, topic_arm_5, topic_arm_6):

    def send_joint_config(topics_list, config_list):
        for topic, value in zip(topics_list, config_list):
            topic.send_message(std_msgs.msg.Float64(value))

    if command.value is None:
        return
    else:
        command_str = command.value.data
    if command_str == last_command_executed.value:
        return

    import collections
    clientLogger.info("ARM received: {}".format(command_str))
    topics_arm = [topic_arm_1, topic_arm_2, topic_arm_3, topic_arm_4, topic_arm_5, topic_arm_6]
    commands_confs = collections.defaultdict(None, {
            "APPROACH": {"TRAY": approach_tray_conf.value},
            "GRASP": {"0": grasp_conf_0.value, "1": grasp_conf_1.value, "2": grasp_conf_2.value, "3": grasp_conf_3.value,
                      "4": grasp_conf_4.value, "5": grasp_conf_5.value, "6": grasp_conf_6.value, "7": grasp_conf_7.value,
                      "8": grasp_conf_8.value, "9": grasp_conf_9.value},
            "DISPOSE": {"TRAY": dispose_tray_conf.value},
            "RESET": reset_conf.value
        })

    # parse command
    split_command = command_str.split('_')
    action = split_command[0]

    if len(split_command) > 1:
        color = split_command[-1]
        new_config = commands_confs[action][color]
    else:
        new_config = commands_confs[action]

    if new_config is not None:
        last_command_executed.value = command_str
        send_joint_config(topics_arm, new_config)
