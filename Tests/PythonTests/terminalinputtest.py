#Alex Black
import sys 						#For command line input
import time 						#Contains delays and whatnot

#Special variables
cameraPort = 0


#Function-input declarations
def help( input ):					#Put all options THEN documentation here, will print help string
	#Put all documentation between the two '''s
	print( '''
+------------+
| -- OPTIONS |
+------------+
--help	     | Prints help function	
--h	     | Prints help function
--camPort    | Define index for prefered connected camera. 0 by default.
''' )
	sys.exit()	

def h( input ):
	help( input )

def camPort( input ):
	global cameraPort
	cameraPort = int( sys.argv[ i + 1 ] )
	return cameraPort

#General information on the inputs and avalible options
inputLength = len( sys.argv ) - 1			#Saves number of inputs, not including name of program (in sys.arg[ 0 ])
posInputs = [ 'h', 'help', 'camPort' ]			#Allowed -- functions

#Parses inputs
i = 1
while i < ( inputLength + 1 ):				#Runs through each option, called functions based off the string will handle whether or not the next value is skipped
	if sys.argv[ i ].startswith( "--" ):
		try:
			if not sys.argv[ i ][ 2: ] == "":
				i = i + eval( sys.argv[ i ][ 2: ] + "(" + str( i ) + ")" )
			else:
				sys.exit( "Missing option after --." )
		except NameError:
			sys.exit( sys.argv[ i ][ 2: ] + " is an invalid option" ) 			
	else:
		print( "Invalid argument: " + sys.argv[ i ] )
	i += 1

print( cameraPort )
