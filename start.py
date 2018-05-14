import subprocess
import sys
import os
import configparser
import argparse
import logging
import signal


import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("betaloop")

class Betaloop:
    def __init__(self, gazebo_assets):
        self.host = "localhost"
        self.gz_port = 11345
        self.gz_assets = gazebo_assets

        signal.signal(signal.SIGINT, self._shutdown)
        self.pids = []

    def _get_env_var(self, name):
        """ Get an environment variable if it exists 
        
        Args:
            name (string): variable to get
        """
        # Copied from https://github.com/wil3/gymfc/blob/master/gymfc/envs/gazebo_env.py
        return os.environ[name] if name in os.environ else ""

    def load_gazebo_vars(self):
        # Copied from https://github.com/wil3/gymfc/blob/master/gymfc/envs/gazebo_env.py

        # TODO is supporting Gazebo 9 just replacing 8->9?
        # Taken from /usr/share/gazebo-8/setup.sh
        ld_library_path = self._get_env_var("LD_LIBRARY_PATH")

        # If loaded previously
        gz_resource =   self._get_env_var("GAZEBO_RESOURCE_PATH")  
        gz_plugins = self._get_env_var("GAZEBO_PLUGIN_PATH")
        gz_models = self._get_env_var("GAZEBO_MODEL_PATH")

        os.environ["GAZEBO_MASTER_URI"] = "http://{}:{}".format(self.host, self.gz_port)
        os.environ["GAZEBO_MODEL_DATABASE_URI"] = "http://gazebosim.org/models"

        # FIXME Remove hardcoded paths and pull this from somewhere so its 
        # cross platform
        os.environ["GAZEBO_RESOURCE_PATH"] = "/usr/share/gazebo-8" + os.pathsep + gz_resource
        os.environ["GAZEBO_PLUGIN_PATH"] = "/usr/lib/x86_64-linux-gnu/gazebo-8/plugins" + os.pathsep + gz_plugins
        os.environ["GAZEBO_MODEL_PATH"] = "/usr/share/gazebo-8/models" + os.pathsep + gz_models

        os.environ["LD_LIBRARY_PATH"] = "/usr/lib/x86_64-linux-gnu/gazebo-8/plugins" + os.pathsep + ld_library_path
        os.environ["OGRE_RESOURCE_PATH"] = "/usr/lib/x86_64-linux-gnu/OGRE-1.9.0"

        # Now load assets

        models = os.path.join(self.gz_assets, "models")
        plugins = os.path.join(self.gz_assets, "plugins", "build")
        worlds = os.path.join(self.gz_assets, "worlds")
        os.environ["GAZEBO_MODEL_PATH"] = "{}:{}".format(models, os.environ["GAZEBO_MODEL_PATH"])
        os.environ["GAZEBO_RESOURCE_PATH"] = "{}:{}".format(worlds, os.environ["GAZEBO_RESOURCE_PATH"])
        os.environ["GAZEBO_PLUGIN_PATH"] = "{}:{}".format(plugins, os.environ["GAZEBO_PLUGIN_PATH"])


    def _start_and_block_until(self, arguments, output_condition):
        p = subprocess.Popen(arguments, shell=False, 
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        self.pids.append(p.pid)
        start_time = time.time()
        while True:
            output = p.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                out = str(output.strip())
                print(out)
                if output_condition in out:
                    break
            if time.time() > start_time + 30:
                raise Execption("Process start timeout")
            rc = p.poll()

    def start_gazebo(self, world, show_gzclient):
        self.load_gazebo_vars()
        #self._start_and_block_until(["gzserver", "--verbose", world], "Connected to gazebo master")
        exe = None
        if show_gzclient:
            exe = "gazebo"
        else:
            exe = "gzserver"
        p = subprocess.Popen([exe, "--verbose", world], shell=False)
        #                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        self.pids.append(p.pid)
        time.sleep(10)

    def start_betaflight(self, elf):
        # Need to wait until uart2 is bound so we cna connect our controller to it
        try:
            self._start_and_block_until([elf], "bind port 5762 for UART2")
        except Exception as e:
            logger.error("Timeout starting betaflight, are you sure you have configured your FC to allow communication to UART2?")
            sys.exit()

    def start_video_receiver(self, vidrecv):
        p = subprocess.Popen([vidrecv], shell=False)
        self.pids.append(p.pid)


    def _shutdown(self, a, b):
        """ Kill the gazebo processes based on the original PID  """
        for pid in self.pids:
            p = subprocess.run("kill {}".format(pid), shell=True)
            logger.info("Killed process {}".format(p))
        sys.exit()


    def start_transmitter(self, transmitter):
        p = subprocess.Popen(["node", transmitter], shell=False)
        self.pids.append(p.pid)


    def start(self, world, elf, transmitter, vidrecv, show_gzclient):
        # Block until connected
        logger.info("Starting Gazebo world {}.".format(world))
        self.start_gazebo(world, show_gzclient)
        time.sleep(5)

        # Now start Betaflight and connect
        logger.info("Starting Betaflight SITL at {}.".format(elf))
        self.start_betaflight(elf)

        # Finally we can connect our radio
        logger.info("Starting the transmitter...")
        self.start_transmitter(transmitter)

        if not show_gzclient:
            logger.info("Starting video receiver {}".format(vidrecv))
            self.start_video_receiver(vidrecv)

        # Keep it up so we can kill with ctrl + c
        while True:
            time.sleep(1)

if __name__ == "__main__":
    if not os.path.exists("config.txt"):
        logger.warn("Could not find configuration file config.txt, fallingback to command line arguments")

    # Load config
    config = configparser.ConfigParser()
    config.read("config.txt")
    gazebo_assets_home = config["Betaloop"]["AeroloopGazeboHome"]
    world =  os.path.join(gazebo_assets_home, "worlds", config["Betaloop"]["World"])
    elf = config["Betaloop"]["BetaflightElf"]
    msp_virtual_radio_home = config["Betaloop"]["MspVirtualRadioHome"]
    transmitter = os.path.join(msp_virtual_radio_home, "emu-dx6-msp.js")

    vidrecv = config["Betaloop"]["Vidrecv"]

    parser = argparse.ArgumentParser("Betaloop")
    parser.add_argument('--gazebo-assets', type=str, default=gazebo_assets_home)
    parser.add_argument('--world', type=str, default=world)
    parser.add_argument('--elf', type=str, default=elf)
    parser.add_argument('--transmitter', type=str, default=transmitter)
    parser.add_argument('--vidrecv', type=str, default=vidrecv)
    parser.add_argument('--gazebo', help="Start in Gazebo, not FPV mode", action="store_true")

    args = parser.parse_args()

    #Make sure they are set
    """
    if not world:
        logger.error("No world specified, please add to config.txt or command line argument")
        sys.exit()
    if not elf:
        logger.error("No location to Betaflight Elf file specified, please add to config.txt or command line argument")
        sys.exit()
    """

    betaloop = Betaloop(args.gazebo_assets)
    betaloop.start(args.world, args.elf, args.transmitter, args.vidrecv, args.gazebo)


