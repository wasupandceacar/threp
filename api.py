from threp import load
from static import init_work_attr

class THReplay():
    def __init__(self, replay_file):
        init_work_attr()
        self.__replay_info=load(replay_file)

    def reload_replay(self, replay_file):
        self.__replay_info = load(replay_file)

    def get_info(self):
        return self.__replay_info

    def getBaseInfo(self):
        return self.__replay_info['base_info']

    def getStageScore(self):
        return self.__replay_info['stage_score']

    def getScreenAction(self):
        return self.__replay_info['screen_action']

    def getKeyboardAction(self):
        return self.__replay_info['keyboard_action']

    def getPlayer(self):
        return self.__replay_info['player']

    def getSlowRate(self):
        return self.__replay_info['slowrate']

    def getDate(self):
        return self.__replay_info['date']

if __name__ == '__main__':
    tr=THReplay('th143_01.rpy')
    print(tr.getBaseInfo())
    print(tr.getStageScore())
    #print(tr.getScreenAction())
    #print(tr.getKeyboardAction())
    print(tr.getPlayer())
    print(tr.getSlowRate())
    print(tr.getDate())