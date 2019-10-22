import winpexpect
import numpy as np
import time
import re

class session:
    def __init__(self):
        xfoil_start_cmd = 'xfoil'
        logfile = open('C:/Users/Thomas/OneDrive/Tieto/Scripts/XFOILsession.txt','w')
        self.proc = winpexpect.winspawn(xfoil_start_cmd, logfile=logfile) 

    def send(self, cmd):
        """Internal function used to send a command to xfoil.
        .. warning::
           This function should generally not be used except internally.
           If some functionality needs to be implemented, let us know 
           instead of simply using :py:func:`send`.
        :param cmd: the command to send, eg 'ALFA' or 'oper'
        :type cmd: str
        :param resulting_prompt: prompt we expect xfoil to display after cmd is sent
        :type resulting_prompt: str
        """
        self.proc.sendline(cmd)
        if cmd == 'init':
            print('INIT sent')

    def alfa(self, a):
        """Run a single angle of attack and return output
        :param a: angle of attack (degrees)
        :type a: float
        :returns: An :py:class:`output` object
        """
        self.send('alfa' + str(a))
        self.proc.expect(['c>'])
        return output(self.proc.before)

    def terminate(self):
        self.proc.terminate()

class output:
    """A class for processing and parsing xfoil output
    Instances of :py:class:`output` are obtained as return values from the :py:class:`session` methods :py:func:`alfa` and :py:func:`cl`.
    """
    def __init__(self, str):
        self.raw = str
        splitstr = '\r\n\r\n'
        last3 = []
        self.data = []
        for i in range(0,3):
            parts = str.rpartition(splitstr)
            last3.append(parts[2])
            str = parts[0]
        for pos, i in enumerate(last3):
            if ('Point added' in i):
                print('Found point added')
                self.point_added = True
                self.data.append(i)
                break
            elif ('VISCAL:' in i):
                print('Convergence failed')
                session.send('init')
                print(last3)
                break
            # elif('BLs will be initialized' in i):
            #     print('Skipping AOA')
            #     break
            else:
                print('Unexpected last3 in output.')
                if pos == 2:
                    print('Error message printed below:')
                    print(last3)

        #we now have data in self.data
        self.converged = 'Convergence failed' not in self.data
        with open('C:/Users/Thomas/OneDrive/Tieto/Scripts/output_xfoil.txt', 'a') as f:
            for i in last3:
                f.write(i)
                f.write('\n')
            f.close()

        def converged(self):
            """:returns: bool telling whether or not xfoil converged"""
            return self.converged 



if __name__ == "__main__":
    session = session()
    session.send('load C:/Users/Thomas/OneDrive/Tieto/Airfoils/S818.dat')
    session.send('mdes')
    session.send('filt')
    session.send('exec')
    session.send(' ')
    session.send('pane')
    session.send('ppar')
    session.send('n')
    session.send('256')
    session.send(' ')
    session.send(' ')
    session.send('oper')
    session.send('iter 250')
    session.send('re 2500000')
    session.send('visc 2500000')
    session.send('pacc')
    session.send('C:/Users/Thomas/OneDrive/Tieto/Airfoils/xfoil/S818_output3.txt')
    session.send(' ')
    time.sleep(2)
    iter_range = np.linspace(0,-20,81)
    # iter_range = iter_range[::-1]
    for i in iter_range:
        session.alfa(i)
    for i in np.linspace(0.25,20,80):
        session.alfa(i)         
    time.sleep(10)
    session.send('pacc')
    session.send('visc')
    session.send(' ')
    session.send('quit')
    session.terminate()
