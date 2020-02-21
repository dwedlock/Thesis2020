import rospy
import time
import csv
from scipy.spatial import distance
from multiprocessing import Process , Queue
from std_msgs.msg import Header
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import GetModelState, GetModelStateRequest, GetLinkState, GetLinkStateRequest
from std_msgs.msg import String

from roslibpy import Message
from roslibpy import Topic

from compas_fab.backends import RosClient





class Odom(Process):
    def __init__(self,queue,queue_two):
        super (Odom,self).__init__()
        #rospy.init_node('odom_pub')

        #odom_pub = rospy.Publisher('/my_odom',Odometry)
        self.queue = queue
        self.queue_two = queue_two
        rospy.wait_for_service('/gazebo/get_model_state')
        
        #rospy.init_node('talker', anonymous=True)
        
        #self.large_x = 0.0
        #self.large_y = 0.0
        #self.large_z = 0.0
        #get_model_srv = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        #self.get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)

        #odom = Odometry()

        #header = Header()

        #header.frame_id = '/odom'

        #model = GetModelStateRequest()
        #self.link = GetLinkStateRequest()

        #model.model_name = 'robot'
        #self.link.link_name = 'wrist_3_link'
        #self.signal = True
        self.queue.put(True)
        #r = rospy.Rate(10) #10Hz publish rate
        #run()
        #print "Odom Client Running "
        self.pub = rospy.Publisher('chatter', String, queue_size=10)
        self.rate = rospy.Rate(1) # 1 = 1 per second 10 = 10hz




    def run(self):
        #while not rospy.is_shutdown():
        #print "Queue RUN "
        #print self.queue.get()
        #truth = self.signal
        #self.queue.put(self.signal)
        #result = get_model_srv(model)
        #time.sleep(1)
        print "Entering While Loop"
        while not rospy.is_shutdown():
            self.hello_str = "hello world %s" % rospy.get_time()
            rospy.loginfo(self.hello_str)
            self.pub.publish(self.hello_str)
            self.rate.sleep()
            print "I am running"


        # print "Odom Client Running "
        # pub = rospy.Publisher('chatter', String, queue_size=10)
        # rate = rospy.Rate(10) # 10hz
        # print "Entering While Loop"
        # while not rospy.is_shutdown():
        #     hello_str = "hello world %s" % rospy.get_time()
        #     rospy.loginfo(hello_str)
        #     self.pub.publish(hello_str)
        #     self.rate.sleep()
        #     print "I am running"



        # with RosClient() as client:
        #     talker = Topic(client, '/chatter', 'std_msgs/String')

        #     while client.is_connected:
        #         talker.publish(Message({'data': 'Hello World!'}))
        #         print('Sending message...')
        #         time.sleep(1)

        #     talker.unadvertise()
        print "Woops we exited the client"

        timer = 0
        truth = self.queue.get()
        print "Im starting the recording loop"
        while(True):
            #print "OR this loop Im in this loop forever"
            time.sleep(.1)
            if timer > 100:
                truth = self.queue.get()
                x = linkresult.link_state.pose.position.x
                    
                    
                y = linkresult.link_state.pose.position.y
                    
                z = linkresult.link_state.pose.position.z
                #print "Do we fail here"
                #print self.queue_two
                #self.queue_two.empty()
                #time.sleep(1)
                #self.queue_two

                self.queue_two.put_nowait(x)
                #print "Do we fail here pass x"
                #ime.sleep(1)
                self.queue_two.put_nowait(y)
                #print "Do we fail here pass y"
                #time.sleep(1)
                self.queue_two.put_nowait(z)
                #time.sleep(1)
                #print "do we fail here"

                timer = 0
            timer = timer +1
            #print "truth Signal"
            #print truth
            if(truth):
                #truth = self.queue.get()
                #self.queue.put(self.signal)
                #print "truth signal"
                #print self.queue.get()
                #print "Signal is True and I am doing stuff"  
                get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
                link = GetLinkStateRequest()

        #model.model_name = 'robot'
                link.link_name = 'wrist_3_link'
                linkresult = get_link_srv(link)
                #print "X",linkresult.link_state.pose.position.x, "Y", linkresult.link_state.pose.position.y, "Z", linkresult.link_state.pose.position.z
                with open('records.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
                    x = linkresult.link_state.pose.position.x
                    
                    
                    y = linkresult.link_state.pose.position.y
                    
                    z = linkresult.link_state.pose.position.z
                    
                    #self.queue_two.put(x)
                    #self.queue_two.put(y)
                    #self.queue_two.put(z)
                    writer.writerow([x,",",y,",",z])
            
                #self.r.sleep() # makes sure 10 hz
            else:
                ()#print "holding"
            

    def stop_record(self):
        #print "Queue Stop "
        #print self.queue.get()
        #print "stopping"
        #self.signal = False
        self.queue.empty()
        self.queue.put(False)
        #print "HOPE UPDATE!!!!!!!!!!!!!!!!!!!!" 
        #print self.queue.get()
        #time.sleep(5)
    
    def start_record(self):
        #print "Queue Start "
        #print self.queue.get()
        #print "starting"
        #self.signal = True
        #self.queue.empty()
        self.queue.put(True)
        #print self.queue.get()
        #time.sleep(5)
        #odom.pose.pose= result.pose
        #odom.twist.twist = result.twist

        #header.stamp = rospy.Time.now()
        #odom.header = header

        #odom_pub.publish(odom)
            #print odom
        #r.sleep() # makes sure 10 hz

    def evaluate(self):
        euclid = 0.0
        #print "QQQQ2222"
        x = self.queue_two.get()
        time.sleep(.01)
        y = self.queue_two.get()
        time.sleep(.01)
        z = self.queue_two.get()
        time.sleep(.01)
        p1 = (0.0,0.0,0.0)
        p2 = (x,y,z)
        #print p2
        euclid = distance.euclidean(p1,p2)
        print "EEEEEEEEEEEEEEEEEEEEEEEEE  Euclidean: ", euclid
        #print self.queue_two.qsize()
        #self.queue_two.empty()
        for x in range(0,self.queue_two.qsize()):
            self.queue_two.get()
            #clears our the queue


        #print self.queue_two.qsize()

        #Clear Queue here if required
        return euclid






