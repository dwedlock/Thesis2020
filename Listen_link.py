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
    print "am I called at all"
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    print data.data
    global recording
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
        #print "Queue RUN "
        #print self.queue.get()
        #truth = self.signal
        #self.queue.put(self.signal)
        #result = get_model_srv(model)
        #timer = 0
        #truth = self.queue.get()
    
    print "Im starting the recording loop"
    #rate = rospy.Rate(10) # 10hz
    get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
    link = GetLinkStateRequest()
    link.link_name = 'wrist_3_link'
    #rospy.init_node('listener', anonymous=True)

    while not rospy.is_shutdown():
            #hello_str = "hello world %s" % rospy.get_time()
            #rospy.loginfo(hello_str)
            #pub.publish(hello_str)
        rospy.Subscriber("writer", String, callback)
        #'filestring'
        rospy.Subscriber("filestring", String, callback_file)
        print "recording ",recording 
        print "file ",file_to_write
        #print "i Received back ", data_return
        #print "Looping"
        time.sleep(.1) 
        linkresult = get_link_srv(link)
        # These values are for each timestep writen to each row
        x = linkresult.link_state.pose.position.x
        y = linkresult.link_state.pose.position.y
        z = linkresult.link_state.pose.position.z
        if recording == True:
            with open(file_to_write, 'a') as csvfile:
                writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
                writer.writerow([x,",",y,",",z])
            
    #                 x = linkresult.link_state.pose.position.x
                    
                    
    #                 y = linkresult.link_state.pose.position.y
                    
    #                 z = linkresult.link_state.pose.position.z
                    
    #                 #self.queue_two.put(x)
    #                 #self.queue_two.put(y)
    #                 #self.queue_two.put(z)
    #                
        ##WITE TO THE CSV/XML file 

        #print "X ", x, "Y ",y, "Z",z
        #listener()
        
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
           
            
        #rate.sleep() # ensures we are saving ever 10




    #         if timer > 100:
    #             truth = self.queue.get()
    #             x = linkresult.link_state.pose.position.x
                    
                    
    #             y = linkresult.link_state.pose.position.y
                    
    #             z = linkresult.link_state.pose.position.z
    #             #print "Do we fail here"
    #             #print self.queue_two
    #             #self.queue_two.empty()
    #             #time.sleep(1)
    #             #self.queue_two

    #             self.queue_two.put_nowait(x)
    #             #print "Do we fail here pass x"
    #             #ime.sleep(1)
    #             self.queue_two.put_nowait(y)
    #             #print "Do we fail here pass y"
    #             #time.sleep(1)
    #             self.queue_two.put_nowait(z)
    #             #time.sleep(1)
    #             #print "do we fail here"

    #             timer = 0
    #         timer = timer +1
    #         #print "truth Signal"
    #         #print truth
    #         if(truth):
    #             #truth = self.queue.get()
    #             #self.queue.put(self.signal)
    #             #print "truth signal"
    #             #print self.queue.get()
    #             #print "Signal is True and I am doing stuff"  
    #             get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
    #             link = GetLinkStateRequest()

    #     #model.model_name = 'robot'
    #             link.link_name = 'wrist_3_link'
    #             linkresult = get_link_srv(link)
    #             #print "X",linkresult.link_state.pose.position.x, "Y", linkresult.link_state.pose.position.y, "Z", linkresult.link_state.pose.position.z

            
    #             #self.r.sleep() # makes sure 10 hz
    #         else:
    #             ()#print "holding"
            

    # def stop_record(self):
    #     #print "Queue Stop "
    #     #print self.queue.get()
    #     #print "stopping"
    #     #self.signal = False
    #     self.queue.empty()
    #     self.queue.put(False)
    #     #print "HOPE UPDATE!!!!!!!!!!!!!!!!!!!!" 
    #     #print self.queue.get()
    #     #time.sleep(5)
    
    # def start_record(self):
    #     #print "Queue Start "
    #     #print self.queue.get()
    #     #print "starting"
    #     #self.signal = True
    #     #self.queue.empty()
    #     self.queue.put(True)
    #     #print self.queue.get()
    #     #time.sleep(5)
    #     #odom.pose.pose= result.pose
    #     #odom.twist.twist = result.twist

    #     #header.stamp = rospy.Time.now()
    #     #odom.header = header

    #     #odom_pub.publish(odom)
    #         #print odom
    #     #r.sleep() # makes sure 10 hz

    # def evaluate(self):
    #     euclid = 0.0
    #     #print "QQQQ2222"
    #     x = self.queue_two.get()
    #     time.sleep(.01)
    #     y = self.queue_two.get()
    #     time.sleep(.01)
    #     z = self.queue_two.get()
    #     time.sleep(.01)
    #     p1 = (0.0,0.0,0.0)
    #     p2 = (x,y,z)
    #     #print p2
    #     euclid = distance.euclidean(p1,p2)
    #     print "EEEEEEEEEEEEEEEEEEEEEEEEE  Euclidean: ", euclid
    #     #print self.queue_two.qsize()
    #     #self.queue_two.empty()
    #     for x in range(0,self.queue_two.qsize()):
    #         self.queue_two.get()
    #         #clears our the queue


    #     #print self.queue_two.qsize()

    #     #Clear Queue here if required
    #     return euclid

if __name__ == '__main__':
  main()



