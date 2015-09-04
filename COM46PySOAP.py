
#------------------------------------------------------------------------------
# These are examples of how to use python and suds to implement a com46 SOAP
# interface using the WSDL from technicolor.
#
# M. Anderson 8 September 2014
#------------------------------------------------------------------------------

import logging
import suds
from suds.client import Client

#------------------------------------------------------------------------------
# Turn on logging to help debug code when necessary
#------------------------------------------------------------------------------

#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

#------------------------------------------------------------------------------

# These four lines (below) are common to all usages
# These two lines are the addresses to the wsdl and the com46 card

com46url = 'http://192.168.3.6:8080'
url = 'file:///Python27/mcb225control.wsdl'

# First we create the client (com46) and read the wsdl then we point the
# client at the com46 card

com46 = Client(url)
com46.set_options(location=com46url)

#print com46


#------------------------------------------------------------------------------
# These commands  have been tested and passed
#------------------------------------------------------------------------------

#print com46.service.Get_COM46_Status()
#print com46.service.Get_Channel_Status(0)
#print com46.service.Get_Channel_Info(5945)
#print com46.service.Get_Tuner_Status(0)
#print com46.service.Get_MCB_Sys_Info()
#print com46.service.Get_MCB_User_Configuration()
#print com46.service.Get_MCB_Health()
#print com46.service.Reset()
#print com46.service.Channel_Close(0)


#------------------------------------------------------------------------------
# This is an examples of how to build complex types using suds. This is a
# Channel_Tune command to the com46. The "ChannelConfigType" (array) is
# built using the suds factory.create function.
#------------------------------------------------------------------------------

# You can use factory.create to create enums with dot notation
# capabilities or you can send the string directly. Examples are:
# tunetest.Protocol_Type = "UDP" 
# tunetest.Protocol_Type = Protocol_Type.UDP
# Both of these lines put the string "UDP" into the array and work
# equally well in this case

Protocol_Type = com46.factory.create("ProtocolTypeEnum")
Security_Mode = com46.factory.create("SecurityModeEnum")
#print Security_Mode

tunetest = com46.factory.create("ChannelConfigType")
#print tunetest

tunetest.Tuner_Number = 0
tunetest.Channel_Object_ID = 4264960
tunetest.IP_Address = "225.0.0.15"
tunetest.Port_Number = 1211
tunetest.Protocol_Type = Protocol_Type.UDP
tunetest.Stream_ID = 111
tunetest.Security_Mode = Security_Mode.None
tunetest.Persistent = "true"

#print com46.service.Channel_Tune(tunetest)

#------------------------------------------------------------------------------

direct_tune = com46.factory.create("DirectTuneType")
#print direct_tune

direct_tune.Tuner_Number = 0
direct_tune.Network_ID = 1
direct_tune.Frequency_Index = 10
#print direct_tune

#print com46.service.Direct_Tune(direct_tune)

#------------------------------------------------------------------------------

# Using the search type "Number" returns the SD channels COID using
# searchtype "Name" returns the HD channels COID

channelsearch = com46.factory.create("ChannelSearchType")
#print channelsearch

searchtype = com46.factory.create("SearchTypeEnum")

#channelsearch.Search_Type = "Number"
#channelsearch.Major_Number = 206
#channelsearch.Minor_Number = 65535
#channelsearch.Name = ""

channelsearch.Search_Type = searchtype.Name
channelsearch.Major_Number = None
channelsearch.Minor_Number = None
channelsearch.Name = "ESPN"

#print com46.service.Channel_Search(channelsearch)

#------------------------------------------------------------------------------

# log level is looking for the name of the module to apply the log level
# setting to. Below is a list that I got from Steve Rhoads at Technicolor
#
#./network/network.c:30:#define MODULE_LTR "n"
#./eapg/apgload.c:29:#define MODULE_LTR "g"
#./eapg/apglock.c:25:#define MODULE_LTR "g"
#./eapg/apgdesc.c:27:#define MODULE_LTR "g"
#./eapg/ddi_apglib.c:43:#define MODULE_LTR  "g"
#./eapg/notification.c:27:#define MODULE_LTR "g"
#./eapg/apgcond.c:27:#define MODULE_LTR "g"
#./eapg/apgheap.c:32:#define MODULE_LTR  "g"
#./eapg/apgsysdep.c:22:#define MODULE_LTR "g"
#./eapg/apgmisc.c:27:#define MODULE_LTR "g"
#./eapg/apgbtree.c:21:#define MODULE_LTR "g"
#./eapg/apgstate.c:32:#define MODULE_LTR "g"
#./eapg/guide.c:24:#define MODULE_LTR "g"
#./eapg/apgunpack.c:24:#define MODULE_LTR "g"
#./eapg/apgquery.c:25:#define MODULE_LTR "g"
#./main/stream.c:89:#define MODULE_LTR "a"
#./main/tuner.c:68:#define MODULE_LTR "a"
#./main/dmx.c:65:#define MODULE_LTR "c"
#./main/filter.c:40:#define MODULE_LTR "a"
#./main/fpga_io.c:30:#define MODULE_LTR "f"
#./main/swm.c:35:#define MODULE_LTR "a"
#./main/main.c:43:#define MODULE_LTR "m"
#./main/sysmon.c:21:#define MODULE_LTR  "m"
#./display/transmit.c:26:#define MODULE_LTR "d"
#./display/grid.c:30:#define MODULE_LTR "d"
#./verifier/events.c:42:#undef MODULE_LTR
#./verifier/events.c:43:#define MODULE_LTR "v"
#./verifier/verifier.c:47:#undef MODULE_LTR
#./verifier/verifier.c:48:#define MODULE_LTR "v"
#./soapservice/soapservice_commands.c:22:#define MODULE_LTR "s"
#./misc/hwlib.c:26:#define MODULE_LTR "h"
#./misc/os.c:30:#define MODULE_LTR "o"


loglevelenum = com46.factory.create("LogLevelEnum")
#print loglevelenum
loglevel = com46.factory.create("LogLevelType")
#print loglevel
loglevel.Module = "s"
loglevel.Level = loglevelenum.Debug

#print com46.service.Log_Level(loglevel)

#------------------------------------------------------------------------------

userconfig = com46.factory.create("UserConfigurationType")
#print userconfig

IPaddrenum = com46.factory.create("IPAddressConfigurationEnum")
#print IPaddrenum


userconfig.System_Integrator_ID = "0123456789"
userconfig.Property_ID = "0123456789"
userconfig.CNR_Low_Threshold = 7.5
#userconfig.Transport_Packet_Threshold = 
userconfig.Time_To_Live = 6
userconfig.IP_Address_Configuration0 = IPaddrenum.Default
#userconfig.Base_IP_Address0 =
#userconfig.Subnet_Mask_Assignment0 =
#userconfig.Default_Gateway_Assignment0 =
#userconfig.IP_Address_Configuration1 =
#userconfig.Base_IP_Address1 =
#userconfig.Subnet_Mask_Assignment1 =
#userconfig.Default_Gateway_Assignment1 =
userconfig.Send_Log_IP_Address = "192.168.20.200"
#userconfig.Utility_Configuration =


print com46.service.Set_MCB_User_Configuration(userconfig)
print com46.service.Get_MCB_User_Configuration()


#------------------------------------------------------------------------------
# These are all the event related commands
#------------------------------------------------------------------------------

eventhandler = com46.factory.create("EventHandlerType")
#print eventhandler

eventhandler.IP_Address = "192.168.3.200"
eventhandler.Port_Number = 1000
eventhandler.Event_Tag = 0
eventhandler.Repeat_Period = 0
eventhandler.Hold_Off_Period = 10
eventhandler.Heart_Beat_Period = 0
#print eventhandler

#print com46.service.Event_Handler(eventhandler)

#------------------------------------------------------------------------------


print com46.service.Get_Event_Status()


#------------------------------------------------------------------------------

testtunerevent0 = com46.factory.create("TEST_TunerEventType")
#print testtunerevent0

testtunerevent0.Tuner_Number = 0
testtunerevent0.Lock_Lost = "true"
testtunerevent0.Transport_Stream_Lost = "true"
testtunerevent0.CNR_Low = "true"
testtunerevent0.No_Video_Content = "true"
testtunerevent0.Coverage_Blackout = "true"
#print testtunerevent0


testtunereventarray = com46.factory.create("TEST_TunerEventArrayType")
#print testtunereventarray

testtunereventarray.Entry = testtunerevent0
#print testtunereventarray

testeventflag = com46.factory.create("TEST_EventStatusType")
#print testeventflag

testeventflag.Event_Message_Test = 0
testeventflag.Event_Message_Available = "true" 
testeventflag.Over_Temp = "true"
testeventflag.Power_Supply_Fault = "true"
testeventflag.Fan_Fault = "true"
testeventflag.LNB_Fault = "true"
testeventflag.Tuner_Events = testtunereventarray
#print testeventflag

#print com46.service.TEST_Event_Flag(testeventflag)

#------------------------------------------------------------------------------

geteventmsg = com46.factory.create("GetEventMessageType")
#print geteventmsg

geteventmsg.Clear_Message_Queue = "true"
#print geteventmsg

#print com46.service.Get_Event_Message(geteventmsg)




#------------------------------------------------------------------------------
# These commands have been tested and have some issues I don't understand yet
#------------------------------------------------------------------------------

# On and Off work using python/suds, flashing returns success but doesn't
# really work the LED toggles off and back on one time, it all works fine
# using eclipse

LEDState = com46.factory.create("LEDStateEnum")
#print LEDState
#print com46.service.LED_Control(LEDState.Flashing)
#print com46.service.LED_Control("Flashing")

#------------------------------------------------------------------------------

com46params = com46.factory.create("COM46ParamType")
#print com46params

# These fields are generic. The first six are unsigned ints the last
# four are strings. Usage is defined in the Technicolor document. At
# this time it looks like only Param1 and Param7 are in use

com46params.Param1 = 0
#com46params.Param2 =
#com46params.Param3 =
#com46params.Param4 =
#com46params.Param5 =
#com46params.Param6 =
#com46params.Param7 =
#com46params.Param8 =
#com46params.Param9 =
#com46params.Param10 =

#print com46params

#print com46.service.Set_COM46_Param(com46params)

