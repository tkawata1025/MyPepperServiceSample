# -*- coding: utf-8 -*-

import qi
import sys

# クラス名は manifest.xml のサービス名と一定していること
class MyService:
    def __init__(self, session):

        self.session = session
        self.logEventName = "%s/log" % self.__class__.__name__
        
        self.memory = self.session.service("ALMemory")
        
        #イベント登録
        self.middlehead_signal = self.memory.subscriber("HandLeftBackTouched").signal
        self.middlehead_signal.connect(self._leftTouchedCallback)
        
        self._logger("MyService Ready..")
                                
    def _leftTouchedCallback(self,value):
        self._logger("_leftTouchedCallback called.") 
        if int(value) > 0:
            tts = self.session.service("ALTextToSpeech")
            tts.say("左手")

    #ログ出力用 (Choregrahe クラス名/event でログメッセージを伝播)
    def _logger(self, msg):
        self.memory.raiseEvent(self.logEventName, msg)
        
    #サービスメソッド
    def myMethod(self,value):
        self._logger("myMethod called.")
        tts = self.session.service("ALTextToSpeech")
        tts.say(value)
    
if __name__ == "__main__":
    app = qi.Application(sys.argv)
    app.start()
    myservice = MyService(app.session)
    app.session.registerService(myservice.__class__.__name__, myservice) 
                
    app.run()   # will exit when the connection is over
