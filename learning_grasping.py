import rospy
import time
import roslaunch
import numpy as np
from scipy.stats import logistic
from geometry_msgs.msg import Pose
from gazebo_msgs.msg import ModelState
from tf.transformations import quaternion_from_euler
from gazebo_msgs.srv import GetModelState, SetModelState
from hbp_nrp_virtual_coach.virtual_coach import VirtualCoach
from smart_grasping_sandbox.smart_grasper import SmartGrasper


def pose_to_array(pose):
	"""
	Helper function that flattens a geometry_msgs.msg.Pose into an array
	"""
	return np.array([pose.position.x, pose.position.y, pose.position.z, pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w])

def array_to_pose(action):
	"""
	Helper function that turns the first 7 entries in an array to a geometry_msgs.msg.Pose
	"""
	pose = Pose()
	pose.position.x = action[0]
	pose.position.y = action[1]
	pose.position.z = action[2]
	pose.orientation.x = action[3]
	pose.orientation.y = action[4]
	pose.orientation.z = action[5]
	pose.orientation.w = action[6]
	return pose


class CEMOptimizer:

	def __init__(self, weights_dim, batch_size=100, deviation=1, deviation_lim=10, rho=0.1, eta=0.1, mean=None):
		self.rho = rho
		self.eta = eta
		self.weights_dim = weights_dim
		self.mean = mean if mean != None else np.zeros(weights_dim)
		self.deviation = np.full(weights_dim, deviation)
		self.batch_size = batch_size
		self.select_num = int(batch_size*rho)
		self.deviation_lim = deviation_lim

	def update_weights(self, weights, rewards):
		rewards = np.array(rewards).flatten()
		weights = np.array(weights)
		sorted_idx = (-rewards).argsort()[:self.select_num]
		top_weights = weights[sorted_idx]
		top_weights = np.reshape(top_weights, (self.select_num, self.weights_dim))
		self.mean = np.sum(top_weights, axis=0) / float(self.select_num)
		self.deviation = np.std(top_weights, axis=0)
		self.deviation[self.deviation > self.deviation_lim] = self.deviation_lim
		if(len(self.deviation)!=self.weights_dim):
			print("dim error")
			print(len(self.deviation))
			print(self.weights_dim)
			exit()

	def sample_batch_weights(self):
		return [np.random.normal(self.mean, self.deviation*(1 + self.eta)) for _ in range(self.batch_size)]

	def get_weights(self):
		return self.mean


def train(object_name):

	def get_object_pose(object_name):
		"""
		Returns the given object's name position and orientation relative to the world's coordinate frame

		:param object_name: String containing the object's name
		"""
		return get_state_srv.call(object_name, "world").pose

	def reset_object_pose(object_name, pose):
		"""
		Resets the give object's name to the new given pose
		"""
		current_model_state = get_state_srv.call(object_name, "world")
		new_model_state = ModelState(model_name=object_name, pose=pose)
		new_model_state.scale = current_model_state.scale
		new_model_state.twist = current_model_state.twist
		new_model_state.reference_frame = 'world'
		set_state_srv.call(new_model_state)

	def compute_euclidean_distance(pose1, pose2):
		"""
		Returns the euclidean distance between two given poses
		"""
		return np.sqrt((pose1.position.x - pose2.position.x)**2 + \
			(pose1.position.y - pose2.position.y)**2 + (pose1.position.z - pose2.position.z)**2)

	def check_stable(joint_names, gripper_pose, object_pose):
		current_min = 500
		positions = []
		velocities = []
		efforts = []
		for k in range(30):
			sgs.move_tip(y=0.03)
			ball_distance = compute_euclidean_distance(gripper_pose, object_pose)
			if k > MIN_LIFT_STEPS and ball_distance < current_min:
				current_min = ball_distance
				break
			if ball_distance > MAX_BALL_DISTANCE:
				break

			time.sleep(0.5)
		robustness = (1/(current_min - 0.18))**2
		return robustness

	def compute_reward(gripper_pose, object_pose):
		return check_stable(hand_joint_names, gripper_pose, object_pose) - compute_euclidean_distance(object_pose, gripper_pose)

	def select_action(pose, weights):
		"""
		Provide the current

		"""
		ob = pose_to_array(pose)
		b1 = np.reshape(weights[0: 7], (7, 1))
		w1 = np.reshape(weights[7: 63], (7, 8))
		b2 = np.reshape(weights[63: 71], (8, 1))
		w2 = np.reshape(weights[71: 135], (8, 8))
		w3 = np.reshape(weights[135: 191], (8, 7))
		b3 = np.reshape(weights[191:], (8, 1))
		ob = np.reshape(ob, (7, 1))

		action_unscaled = logistic.cdf(np.dot(w1, logistic.cdf(np.dot(w2, logistic.cdf(np.dot(w3, ob) - b3)) - b2)) - b1)
		action = tray_boundaries_low + action_unscaled*(tray_boundaries_high - tray_boundaries_low)
		return array_to_pose(action.flatten())

	def start_experiment(experiment_id):
		# Instantiate Virtual Coach and launch Experiment
		vc = VirtualCoach(environment='local', storage_username='nrpuser')
		sim = vc.launch_experiment(experiment_id)

		# roslaunch fh_desc controllers.launch
		fh_desc_launch_file = "/home/akl-ma/.opt/nrpStorage/{}/controllers.launch".format(experiment_id)
		uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
		roslaunch.configure_logging(uuid)
		launch = roslaunch.parent.ROSLaunchParent(uuid, [fh_desc_launch_file])
		launch.start()
		time.sleep(10)

		sim.start()
		return sim

	def test():
		W = opt.get_weights()
		observation = get_object_pose()
		accreward = 0
		action = select_action(observation, W)
		observation, reward, done, info = env.step(action)
		accreward += reward
		print("test end with reward: {}".format(accreward))

	num_episodes = 100
	MIN_LIFT_STEPS = 1
	MAX_BALL_DISTANCE = 0.4
	experiment_id = 'GoogleGrasping_1'

	# The reset pose the robot returns to after each attempt
	robot_reset_position = np.array([0.0, 1.0, 1.5])
	robot_reset_orientation = quaternion_from_euler(-np.pi/2, 0, 0)
	robot_reset_pose = array_to_pose(np.append(robot_reset_position, robot_reset_orientation))
	
	get_state_srv = rospy.ServiceProxy("/gazebo/get_model_state", GetModelState)
	set_state_srv = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)
	hand_joint_names = ["H1_F1J1", "H1_F1J2", "H1_F1J3", "H1_F2J1", "H1_F2J2", "H1_F2J3", "H1_F3J1", "H1_F3J2", "H1_F3J3"]
	tray_boundaries_high = np.reshape(np.array([0.4, 1.15, 1.3, 1, 1, 1, 1]), (7, 1))
	tray_boundaries_low = np.reshape(np.array([-0.4, 0.6, 1.15, -1, -1, -1, -1]), (7, 1))

	weights_dim = 7*1 + 8*7 + 8*1 + 8*8 + 8*7 + 8*1
	opt = CEMOptimizer(weights_dim, batch_size=100, rho=0.1, eta=0.3, deviation=1, deviation_lim=20)
	sim = start_experiment(experiment_id)
	sgs = SmartGrasper()
	sgs.open_hand()
	sgs.move_tip_absolute(robot_reset_pose)

  	for ep in range(num_episodes):
		print("Episode Number:  {}".format(ep))
		weights = opt.sample_batch_weights()
		rewards = []
		opt.eta *= 0.99
		print("deviation mean = {}".format(np.mean(opt.deviation)))
		
		for b in range(opt.batch_size):
			accreward = 0
			observation = get_object_pose(object_name)
			action = select_action(observation, weights[b])

			print "==========================="
			print "Episode # {}, Attempt # {}".format(ep + 1, b + 1)
			print action
			
			
			# correct action orientation
			action.orientation.x = robot_reset_orientation[0]
			action.orientation.y = robot_reset_orientation[1]
			action.orientation.z = robot_reset_orientation[2]
			action.orientation.w = robot_reset_orientation[3]

			# move to pose and pick
			sgs.open_hand()
			time.sleep(1)
			sgs.move_tip_absolute(action)
			time.sleep(1)
			sgs.check_fingers_collisions(False)
			time.sleep(1)
			sgs.close_hand()
			time.sleep(1)

			reward = compute_reward(action, observation)
			sgs.open_hand()
			sgs.check_fingers_collisions(True)

			print "Reward: {}".format(reward)
			print "==========================="

			print " <<<< RESET POSE >>>>"
			# reset robot pose
			sgs.move_tip_absolute(robot_reset_pose)

			rewards.append(reward)
		opt.update_weights(weights, rewards)

if __name__ == '__main__':
	train('cricket_ball')
