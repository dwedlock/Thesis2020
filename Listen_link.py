import rospy
import time
import csv
from scipy.spatial import distance
from multiprocessing import Process , Queue
from std_msgs.msg import Header
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import GetModelState, GetModelStateRequest, GetLinkState, GetLinkStateRequest
from std_msgs.msg import String

recording = False
file_to_write = ""

def callback(data):
    #print "Checking if I should record"
    global recording
    rospy.loginfo(rospy.get_caller_id() + "Action %s", data.data)
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

def main():
    global recording
    rospy.init_node('listener', anonymous=True)
    rospy.wait_for_service('/gazebo/get_model_state')
        #while not rospy.is_shutdown():
    print "Im starting the recording loop"
    #rate = rospy.Rate(10) # 10hz
    get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
    link = GetLinkStateRequest()
    link.link_name = 'wrist_3_link'
    #rospy.init_node('listener', anonymous=True)

    while True:
            #hello_str = "hello world %s" % rospy.get_time()
            #rospy.loginfo(hello_str)
            #pub.publish(hello_str)
        rospy.Subscriber("writer", String, callback)
        #'filestring'
        rospy.Subscriber("filestring", String, callback_file)

        #print "i Received back ", data_return
        #print "Looping"
        time.sleep(.1) 
        linkresult = get_link_srv(link)
        # These values are for each timestep writen to each row
        x = linkresult.link_state.pose.position.x
        y = linkresult.link_state.pose.position.y
        z = linkresult.link_state.pose.position.z
        if recording == True:
            print "recording ",recording,"file ",file_to_write
            
            with open(file_to_write, 'a') as csvfile:
                writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
                writer.writerow([x,",",y,",",z])

if __name__ == '__main__':
  main()



