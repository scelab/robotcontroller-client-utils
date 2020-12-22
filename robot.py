import jtalk
import client
import posedef
import random
import json
import threading
import time
from pydub import AudioSegment

class Robot(object):
    """
    Sota(CommU)を操作するためのクラス
    """
    def __init__(self, ip, robot_id):
        self.robot_id = robot_id
        self.ip = ip
        self.wav_port  = 22222
        self.pose_port = 22223
        self.led_port  = 22224
        self.read_port = 22225
        self.is_moving = False
    
    def say(self, text, speed=1.0, emotion='normal'):
        """
        発話させる。
        """
        output_file = '{}_say.wav'.format(self.robot_id)
        jtalk.make_wav(text, speed, emotion, output_file)
        with open(output_file, 'rb') as f:
            data = f.read()
            client.send(self.ip, self.wav_port, data)
        sound = AudioSegment.from_file(output_file, 'wav')
        return sound.duration_seconds

    def do_random_pose(self, speed=1.0):
        """
        posedefに定義されているBASE_MAPSからランダムに一つを選択し、そのポーズをする。
        speedはポーズの早さ。msec = 1000/speed
        speedが1.0なら1000msecで動作する。
        """
        base_map = random.choice(posedef.BASE_MAPS)
        msec = int(1000 / speed)
        pose = dict(msec=msec, map=base_map)
        data = json.dumps(pose).encode('utf-8')
        client.send(self.ip, self.pose_port, data)
        return msec

    def keep_moving(self, speed=1.0):
        """
        これを実行すると一定間隔でランダムなポーズを実行し続ける。
        stop_movingで止まる。
        """
        threading.Thread(target=self.__moving, args=(speed,)).start()

    def __moving(self, speed=1.0):
        self.is_moving = True
        while self.is_moving:
            self.do_random_pose(speed)
            sec = 1.0 / speed
            time.sleep(sec)
        
    def stop_moving(self):
        self.is_moving = False

    def reset_pose(self, speed=1.0):
        """
        ポーズをホームポジションに戻す。
        """
        home_map = posedef.HOME_MAP
        msec = int(1000 / speed)
        pose = dict(msec=msec, map=home_map)
        data = json.dumps(pose).encode('utf-8')
        client.send(self.ip, self.pose_port, data)

#
# 実行例
#
if __name__ == '__main__':
    r1 = Robot('192.168.11.8', 'R1')
    t = r1.say('おはようございます。今日はいい天気ですね。こんな日はどこかに出かけたくなりますね。', emotion='happy')
    r1.keep_moving()
    print(t)
    time.sleep(t)
    r1.stop_moving()
    r1.reset_pose()
