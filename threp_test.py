import os
import pytest
import numpy as np

from threp import THReplay

replays_data = np.load('rep_tst/rep_data.npy', allow_pickle=True).item()

@pytest.mark.parametrize('replay, rp', [(replay, THReplay(os.path.join('rep_tst', replay))) for replay in replays_data.keys()])
class TestReplay:
    def test_BaseInfo(self, replay, rp):
        assert rp.getBaseInfo() == replays_data[replay]['base_info']

    def test_BaseInfoDic(self, replay, rp):
        assert rp.getBaseInfoDic() == replays_data[replay]['base_infos']

    def test_StageScore(self, replay, rp):
        assert rp.getStageScore() == replays_data[replay]['stage_score']

    def test_ScreenAction(self, replay, rp):
        assert rp.getScreenAction() == replays_data[replay]['screen_action']

    def test_Player(self, replay, rp):
        assert rp.getPlayer() == replays_data[replay]['player']

    def test_SlowRate(self, replay, rp):
        assert rp.getSlowRate() == replays_data[replay]['slowrate']

    def test_Date(self, replay, rp):
        assert rp.getDate() == replays_data[replay]['date']

    def test_FrameCount(self, replay, rp):
        assert rp.getFrameCount() == replays_data[replay]['frame_count']

    def test_Z(self, replay, rp):
        assert rp.getZ() == replays_data[replay]['z_frame']

    def test_X(self, replay, rp):
        assert rp.getX() == replays_data[replay]['x_frame']

    def test_C(self, replay, rp):
        assert rp.getC() == replays_data[replay]['c_frame']

    def test_Shift(self, replay, rp):
        assert rp.getShift() == replays_data[replay]['shift_frame']

    def test_Error(self, replay, rp):
        assert rp.getError() == replays_data[replay]['error']