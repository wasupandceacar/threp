from .decode import load
from .static import init_work_attr

class THReplay:
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

    def getFrameCount(self):
        return self.__replay_info['frame_count']

    def getError(self):
        return self.__replay_info['error']

    def getZ(self):
        return self.__replay_info['z_frame']

    def getX(self):
        return self.__replay_info['x_frame']

    def getC(self):
        return self.__replay_info['c_frame']

    def getShift(self):
        return self.__replay_info['shift_frame']