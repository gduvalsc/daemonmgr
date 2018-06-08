import argparse, json, os, sys, syslog, pickle, subprocess, signal

def wlog(m):
   print(m)
   syslog.syslog(m)
   
def getprocesses():
   process = subprocess.Popen(['ps', '-eo' ,'pid,args'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   stdout, notused = process.communicate()
   r=[]
   for line in stdout.splitlines()[1:]:
      tline = line.lstrip().split(' ') if type(line) == type('') else line.decode().lstrip().split(' ')
      r.append((tline[0], ' '.join(tline[1:])))
   return r

def isstarted(daemon):
   name=daemons[daemon]['name']
   try:
      f=open("/var/log/" + daemon + ".pid", "r")
      pid = f.read()
      f.close()
      started = False
      for p in getprocesses():
         if p[0] == pid and p[1] == name: started = True
   except:
      started = False
   return started


parser = argparse.ArgumentParser()
parser.add_argument('--version', action = 'version', version='0.00')
parser.add_argument('-start', action = 'store_true', dest='start', help='Start daemon if not started')
parser.add_argument('-stop', action = 'store_true', dest='stop', help='Stop daemon if started')
parser.add_argument('-restart', action = 'store_true', dest='restart', help='Restart daemon')
parser.add_argument('-status', action = 'store_true', dest='status', help='Show daemon status')
parser.add_argument('-register', action = 'store_true', dest='register', help='Register daemon')
parser.add_argument('-unregister', action = 'store_true', dest='unregister', help='Unregister daemon')
parser.add_argument('-list', action = 'store_true', dest='list', help='List daemons')
parser.add_argument('--daemon', action = 'store', dest='daemon', default='', help='Daemon name')
parser.add_argument('--stdout', action = 'store', dest='stdout', default='', help='Standard output redirection')
parser.add_argument('--stderr', action = 'store', dest='stderr', default='', help='Standard error redirection')
parser.add_argument('--command', action = 'store', dest='command', default='', help='Command to be daemonized')
parser.add_argument('--name', action = 'store', dest='name', default='', help='Process name')
args = parser.parse_args()

daemons = dict()
try:
   f = open("/var/log/daemonmgr", "rb")
   daemons = pickle.load(f)
   f.close()
except:
   pass

if not args.list and not args.register and not args.unregister and not args.start and not args.stop and not args.restart and not args.status:
   parser.print_help()

if args.register:
   if not args.daemon:
      wlog('*** --daemon parameter is mandatory with -register option')
      exit(1)
   if not args.stdout:
      wlog('*** --stdout parameter is mandatory with -register option')
      exit(1)
   if not args.stderr:
      wlog('*** --stderr parameter is mandatory with -register option')
      exit(1)
   if not args.command:
      wlog('*** --command parameter is mandatory with -register option')
      exit(1)
   if not args.name:
      wlog('*** --name parameter is mandatory with -register option')
      exit(1)
   daemons[args.daemon]=dict(stdout=args.stdout, stderr=args.stderr, command=args.command, name=args.name)

if args.unregister:                                                                                                         
   if not args.daemon:                                                                                                      
      wlog('*** --daemon parameter is mandatory with -unregister option')                                                     
      exit(1)                                                                                                               
   del daemons[args.daemon]                                                                                                 

if args.list:                                                                                                               
   if not args.daemon:                                                                        
      for d in daemons.keys(): wlog('Daemon: ' + d + ', Parameters: ' + str(daemons[d]))      
   else:                                                                                      
      wlog('Daemon: ' + args.daemon + ', Parameters: ' + str(daemons[args.daemon]))           

if args.register or args.unregister:                                                          
   f=open("/var/log/daemonmgr", "wb")                                                             
   pickle.dump(daemons, f)                                                                    
   f.close()                                                                                  

if args.start:                                                                                
   if not args.daemon:                                                                        
      wlog('*** --daemon parameter is mandatory with -start option')                       
      exit(1)
   if isstarted(args.daemon):                                                                
      wlog('*** Daemon is already started!')                       
      exit(1)
   command=daemons[args.daemon]['command'].split(' ')                                         
   stdout = open(daemons[args.daemon]['stdout'], "wb")
   stderr = open(daemons[args.daemon]['stderr'], "wb")
   pid = subprocess.Popen(command, stdout=stdout, stderr=stderr).pid                                        
   f=open("/var/log/" + args.daemon + ".pid", "w")                                            
   f.write(str(pid))                                                                    
   f.close()                                                                            

if args.stop:
   if not args.daemon:                                                                        
      wlog('*** --daemon parameter is mandatory with -stop option')                       
      exit(1)
   if isstarted(args.daemon):
      f=open("/var/log/" + args.daemon + ".pid", "r")
      pid = f.read()
      f.close()
      os.kill(int(pid), signal.SIGINT)

if args.restart:
   if not args.daemon:                                                                        
      wlog('*** --daemon parameter is mandatory with -restart option')                       
      exit(1)
   if isstarted(args.daemon):
      f=open("/var/log/" + args.daemon + ".pid", "r")
      pid = f.read()
      f.close()
      os.kill(int(pid), signal.SIGINT)
   command=daemons[args.daemon]['command'].split(' ')                                         
   stdout = open(daemons[args.daemon]['stdout'], "wb")
   stderr = open(daemons[args.daemon]['stderr'], "wb")
   pid = subprocess.Popen(command, stdout=stdout, stderr=stderr).pid                                        
   f=open("/var/log/" + args.daemon + ".pid", "w")                                            
   f.write(str(pid))                                                                    
   f.close()                                                                            

if args.status:
   if not args.daemon:                                                                        
      for d in daemons.keys():
         if isstarted(d): print("Daemon: " + d + ", status: started")
         else: print("Daemon: " + d + ", status: stopped")
   else:
      if isstarted(args.daemon): print("Daemon: " + args.daemon + ", status: started")
      else: print("Daemon: " + args.daemon + ", status: stopped")
