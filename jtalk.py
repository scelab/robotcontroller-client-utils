import subprocess
import os.path

# OpenJTalkをインストールしたパス
OPENJTALK_BINPATH = '/usr/bin'
OPENJTALK_DICPATH = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
OPENJTALK_VOICEPATH = '/usr/share/hts-voice/mei/mei_{emotion}.htsvoice'

def make_wav(text, speed=1.0, emotion='normal', output_file='__temp.wav', output_dir=os.getcwd()):
    """
    OpenJTalkを使ってmeiの声で音声合成してwavファイルを作る関数。
    引数emotionには'normal', 'happy', 'bashful', 'angry', 'sad'のいずれかを指定可能。
    """
    open_jtalk = [OPENJTALK_BINPATH + '/open_jtalk']
    mech = ['-x', OPENJTALK_DICPATH]
    htsvoice = ['-m', OPENJTALK_VOICEPATH.format(emotion=emotion)]
    speed = ['-r', str(speed)]
    outwav = ['-ow', os.path.join(output_dir, output_file)]
    cmd = open_jtalk + mech + htsvoice + speed + outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(text.encode('utf-8'))
    c.stdin.close()
    c.wait()

if __name__ == '__main__':
    make_wav("今日はいい天気ですね。こんな日はどこかに出かけたくなりますね。", speed=0.8, emotion='happy', output_path='/mnt/c/Users/tiio/Downloads')