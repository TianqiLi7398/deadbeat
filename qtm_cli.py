"""
qtm_cli.py

Lightweight QTM commandline interface

This is really a bunch of test-code snippets that have been given names
and set up to work for accessing QTM manager via instances of the qualisys.QTM class.

All non-streaming traffic is captured in the the .h (history) member 
variable, which may be used for post-mortem analysis of communication.
"""

from cmd import Cmd
from time import time as now, sleep
from sys import stdout
from gzip import open as gzipOpen
from yaml import dump as yamlDump

from pylab import figure, clf, subplot, title, plot, axis, grid, draw

execfile('qualisys.py')

class QTM_CLI(Cmd):
  def __init__(self):
    Cmd.__init__(self)
    self.qtm = QTM()
    self.prompt = "QTM>> "
    self.h = []
  
  def do_cmd( self, line ):
    "Send a QTM command"
    print 'cmd>>',line.strip()
    self.qtm.command( line.strip() )
    self.h.append('cmd --> '+line)
    self.do_tcp('')
    
  def do_tcp( self, line ):
    "Parse all pending TCP inputs"
    print "do_tcp() packets:"
    if not self.qtm.isConnected():
      print "NOT CONNECTED"
      return
    pkt = 1
    while pkt:
      pkt = self.qtm.ptcp.next()
      print 'do_tcp() pkt =',pkt
      self.h.append(pkt)
  
  def do_udp( self, line ):
    "Parse all pending UDP inputs"
    print "UDP:"
    pkt = 1
    while pkt:
      pkt = self.qtm.pudp.next()
      print pkt
      self.h.append(pkt)
      
  def do_discoverAndConnect( self, line ):
    "Do a discovery based connect on specified network address"
    line = line.strip()
    if not line:
      line = "<broadcast>"
    print "Discovering on '%s'" % line
    self.qtm.connectOnNet(line)
    return self.do_cmd("Version 1.9")
  
  def do_streamAllUdp( self, line ):
    "Stream data in over UDP; by default use 2D"
    if not line:
      line = "2D"
    self.do_cmd("StreamFrames AllFrames UDP:%d %s" 
      % (self.qtm.udp.getsockname()[1],line))
    for k in xrange(10):
      pkt = self.qtm.pudp.next()
      print 'do_streamAllUdp() pkt =',pkt
      self.h.append(pkt)
    self.do_cmd("StreamFrames Stop")
  
  def do_streamAllTcp( self, line ):
    "Stream data in over TCP; by default use 2D"
    if not line:
      line = "2D"
    self.do_cmd("StreamFrames AllFrames %s" 
      % line)
    for k in xrange(10):
      pkt = self.qtm.ptcp.next()
      print 'do_streamAllTcp() pkt =',pkt
      self.h.append(pkt)
    self.do_cmd("StreamFrames Stop")
  
  def do_XX( self, line ):
    """Exit command loop without closing sockets
    
    Use: cli.cmdloop() to continue where you left off.
    """
    return True
    
  def do_2Dplot( self, line ):
    line = line.strip()
    if not line:
      dur = 5
    else:
      dur = float(line) 
    #self.do_cmd("StreamFrames AllFrames UDP:%d 2D" 
    #  % (self.qtm.udp.getsockname()[1]))
    self.do_cmd("StreamFrames AllFrames 2D")
    t0 = now()
    t1 = t0
    last = t1-1
    plt = []
    import matplotlib as mpl
    mpl.interactive('on')
    f = figure(1)
    f.set(visible=False)
    clf()
    nn = 0
    while t1-t0 < dur:
      t1 = now()
      #pkt = self.qtm.pudp.next()
      pkt = self.qtm.ptcp.next()
      self.h.append(pkt)
      if not isinstance(pkt,DataPacket):
        print "not data packet:"
        print pkt
        continue
      if not isinstance(pkt.comp[0],C_2D):
        print "not 2D data packet"
        continue
      stdout.write('.'); stdout.flush()
      nn += 1
      if t1 - last<0.2:
        continue
      print nn
      last = t1
      while len(plt)<len(pkt.comp[0].status):
        plt.append(None)
      for n,s in enumerate(pkt.comp[0].status):
        subplot(1,len(plt),n+1)
        title("Camera %d time %d frame %d" % (n,pkt.time,pkt.frame))
        if plt[n] is not None:
          hnd = plt[n]
        else:
          print "New 2D plot for ",n
          hnd = plot( [0,1.3e5], [0,1.3e5], 'o')[0]
          axis('scaled')
          grid(1)
          plt[n] = hnd
        xys = pkt.comp[0].cam[n]
        if len(xys)==0:
          hnd.set(xdata=[],ydata=[])
          print "WARNING: empty cam payload"
          continue
        hnd.set(xdata = xys['x'], ydata=xys['y'])          
      f.set(visible=True)
      draw()
    self.do_cmd("StreamFrames Stop")

  def do_capture( self, line ):
    "Capture 2D and 3D data to files: <duration> <filename-prefix>"
    dur,fn = line.strip().split(" ")
    dur = float(dur)
    self.do_cmd("StreamFrames AllFrames UDP:%d 2D 3DNoLabels" 
      % (self.qtm.udp.getsockname()[1]))
    while self.qtm.ptcp.next(): 
      pass
    t0 = now()
    t1 = t0
    d2 = []
    d3 = []
    tic = t0
    while t1-t0<dur:
      pkt = self.qtm.pudp.next()
      # self.h.append(pkt) # log data packets
      if not isinstance(pkt,DataPacket):
        break        
      stdout.write("\r%6d 2D %6d 3D" % (len(d2),len(d3)))
      stdout.flush()
      for c in pkt.comp:
        if isinstance(c,C_2D):
          for n,cam in enumerate(c.cam):
            for row in cam:
              d2.append([pkt.frame, pkt.time, n ]+list(row))
        else:
          for row in c.mrk:
            d3.append([pkt.frame, pkt.time]+list(row))
      t1 = now()
      if t1-tic>1:
        print " %.2f" %(t1-t0)
        tic = t1
    print " %.2f\n" %(t1-t0)
    self.do_cmd("StreamFrames Stop")
    f2 = gzipOpen(fn+".2D.csv.gz","w")
    for row in d2:
      f2.write(", ".join([ str(long(x)) for x in row ])+"\n")
    f2.close()
    f3 = gzipOpen(fn+".3D.csv.gz","w")
    for row in d3:
      f3.write(", ".join([ str(float(x)) for x in row ])+"\n")
    f3.close()
  
  def emptyline( self ):
    print "Wazzup?"
    
  def do_3Dplot( self, line ):
    line = line.strip()
    if not line:
      dur = 10
    else:
      dur = float(line) 
    self.do_cmd("StreamFrames AllFrames UDP:%d 3DNoLabels" 
      % (self.qtm.udp.getsockname()[1]))
    t0 = now()
    t1 = t0
    last = t1-1
    plan = ['xy','zy','xz']
    nn = 0
    f = figure(4)
    f.set(visible=False)
    clf()
    plt = []
    for n,ax in enumerate(plan):
      subplot(2,2,n+1)
      plt.append( plot( [-1500,1500], [-1500,1500], 'o')[0] )
      xlabel(ax[0].upper())
      ylabel(ax[1].upper())
      axis('scaled')
      grid(1)
    f.set(visible=True)
    draw()
    while t1-t0 < dur:
      t1 = now()
      pkt = self.qtm.pudp.next()
      self.h.append(pkt)
      if not isinstance(pkt,DataPacket):
        continue
      if not isinstance(pkt.comp[0],C_3D_NoLabel):
        continue
      stdout.write('.'); stdout.flush()
      nn += 1
      if t1 - last<0.2:
        continue
      print nn
      last = t1
      mrk = pkt.comp[0].mrk
      f.set(visible=False)
      subplot(2,2,1)
      title("3D time %d frame %d" % (pkt.time,pkt.frame))
      for p,ax in zip(plt,plan):
        p.set(xdata = mrk[ax[0]], ydata=mrk[ax[1]])
      f.set(visible=True)
      draw()
      sleep(0.01)
    self.do_cmd("StreamFrames Stop")

  def do_serverConnect( self, line ):
    "Connect directly to specified server"
    line = line.strip()
    print "Connecting to '%s'" % line
    if not line:
      print "--> ERROR: need a host unicast address"
      return
    self.qtm.connect(line)
    return self.do_cmd("Version 1.9")

  def do_getParameters( self, line ):
    "Get QTM parameters; default is All"
    if not line:
      line = "All"
    self.do_cmd("GetParameters %s" 
      % (line))
    pkt = self.qtm.pudp.next()
    print 'do_getParameters() pkt =',pkt
    self.h.append(pkt)
  
  def do_quit( self, line ):
    "Exit the QTM commandline"
    self.qtm.close()
    return True
  
  def do_help( self, line ):
    "Provide online help"
    Cmd.do_help(self,line)
  
  def do_paramXML( self, line ):
    "Push XML parameters into QTM"
    line = line.strip()
    if line[0] is not "'" or line[-1] is not "'":
      print "XML must be provided as a single quoted string"
    line = eval(line)
    print "Sending:"
    print line
    self.qtm.sendParamXML(line)
    self.h.append("XML --> "+repr(line))
    return self.do_tcp("")
    
  def do_EOF( self, line ):
    "Synonym for 'quit'"
    return self.do_quit(line)
    
if __name__=="__main__":
  cli = QTM_CLI()
  cli.cmdloop()

