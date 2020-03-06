import rospy
import time
import csv
from scipy.spatial import distance
from multiprocessing import Process , Queue
from std_msgs.msg import Header
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import GetModelState, GetModelStateRequest, GetLinkState, GetLinkStateRequest
from std_msgs.msg import String
this_check_move = 0.0 
last_check_move = 0.0 
recording = False
file_to_write = ""

def callback(data):
    #print "Checking if I should record"
    global recording
    #rospy.loginfo(rospy.get_caller_id() + "Action %s", data.data)
    #print data.data
    
    if data.data == "start":
        recording = True
    if data.data == "stop":
        recording = False

    return data.data

def callback_file(data_file):
    global file_to_write
    file_to_write = data_file.data
    print file_to_write

def call_feedback(data_feedback):
    print "Im being called"
    #rospy.loginfo(rospy.get_caller_id() + "getModelState %s", data_feedback)
    #print data_feedback

def main():
    global recording
    global this_check_move
    global last_check_move
    rospy.init_node('listener', anonymous=True)
    rospy.wait_for_service('/gazebo/get_model_state')
    
        #while not rospy.is_shutdown():
    print "Im starting the recording loop"
    #rate = rospy.Rate(10) # 10hz
    get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
    link = GetLinkStateRequest()
    link.link_name = 'wrist_3_link'

    get_model_srv = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
    model = GetModelStateRequest()
    model.model_name = 'robot'
    #rospy.init_node('listener', anonymous=True)

    while True:
            #hello_str = "hello world %s" % rospy.get_time()
            #rospy.loginfo(hello_str)
            #pub.publish(hello_str)
        #rospy.Subscriber("status",String,call_feedback)

        rospy.Subscriber("writer", String, callback)
        #'filestring'
        rospy.Subscriber("filestring", String, callback_file)
        
        
        #print "i Received back ", data_return
        #print "Looping"
        time.sleep(.1) 
        linkresult = get_link_srv(link) # we use for the link
        modelresult = get_model_srv(model) # robot will not move much in this example 
        #print modelresult.pose.position.x
        # These values are for each timestep writen to each row
        x = linkresult.link_state.pose.position.x
        this_check_move = x
        we_moved = False
        diff = abs(last_check_move - this_check_move) 
        if diff > 0.0001:
            we_moved = True
        y = linkresult.link_state.pose.position.y
        z = linkresult.link_state.pose.position.z
        print "recording",recording,"we moved", we_moved
        if recording == True and we_moved == True:
            print "We moved and are recording ",recording,"file ",file_to_write
            
            with open(file_to_write, 'a') as csvfile:
                writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
                writer.writerow([x,",",y,",",z])
        last_check_move = this_check_move

if __name__ == '__main__':
  main()



