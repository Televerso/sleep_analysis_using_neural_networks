from collections import Counter

import numpy as np

from src.utils.config_readers.SleepAnalyzerConfig import SleepAnalyzerConfig
from src.utils.data_structures.SleepTime import SleepTime

class SleepAnalyzer_v1:
    def __init__(self, pose_array, movement_intensity_array, is_present_array, starting_time : SleepTime, framerate, duration, config : SleepAnalyzerConfig):
        self.config = config

        self.movement_intensity = movement_intensity_array
        self.is_present = is_present_array
        self.poses = pose_array

        self.stage_array = np.empty(shape=movement_intensity_array.shape)
        self.stage_dict = dict()
        self.epoch_len = int(self.config.epoch_len*framerate)

        self.starting_time = starting_time
        self.record_len_in_sec = duration

        self._calc_sleep_stage()
        self._get_stage_dict()

        self.sleep_duration_in_sec = self.record_len_in_sec - int(len(self.stage_array[self.stage_array == "WAKE"])/framerate)


    def _calc_sleep_stage(self):
        epoch_len = self.epoch_len
        # Заполняем массив данных значениями соответствующими небыстрому сну
        self.stage_array = np.array(["NREM" for i in range(len(self.movement_intensity))], dtype=str)

        # На промежутках
        for i in range(0, self.stage_array.shape[0], epoch_len):
            left_border = i-epoch_len//2 if (i-epoch_len//2) > 0 else i
            right_border = i+epoch_len//2 if (i+epoch_len//2) < len(self.stage_array) else len(self.stage_array)

            if not min(self.is_present[left_border:right_border]):
                self.stage_array[left_border:right_border] = "WAKE"
            elif (np.sum(self.movement_intensity[left_border:right_border])/len(self.movement_intensity[left_border:right_border]) >=
                  self.config.wake_threshold):
                self.stage_array[left_border:right_border] = "WAKE"
            elif (self.config.wake_threshold >
                  np.sum(self.movement_intensity[left_border:right_border])/len(self.movement_intensity[left_border:right_border]) >
                  self.config.movement_threshold):
                self.stage_array[left_border:right_border] = "REM"

        return self.stage_array

    def _get_stage_dict(self):

        prev_state = ""
        self.stage_dict[str(self.starting_time-1)] = 'START'
        for i in range(self.stage_array.shape[0]):

            if self.stage_array[i] == "WAKE":
                if prev_state != "WAKE":
                    time = self.starting_time + (i/len(self.stage_array))*self.record_len_in_sec
                    self.stage_dict[str(time)] = "WAKE"
                prev_state = "WAKE"

            elif self.stage_array[i] == "REM":
                if prev_state != "REM":
                    time = self.starting_time + (i / len(self.stage_array)) * self.record_len_in_sec
                    self.stage_dict[str(time)] = "REM"
                prev_state = "REM"

            elif self.stage_array[i] == "NREM":
                if prev_state != "NREM":
                    time = self.starting_time + (i / len(self.stage_array)) * self.record_len_in_sec
                    self.stage_dict[str(time)] = "NREM"
                prev_state = "NREM"
        self.stage_dict[str(self.starting_time + self.record_len_in_sec)] = 'END'
        return self.stage_dict

    def _calc_TST(self):
        return self.sleep_duration_in_sec/3600

    def _calc_REM(self):
        return (np.sum(self.stage_array[:]=="REM") / np.sum(self.stage_array != "WAKE")) * self._calc_TST()

    def _calc_N_REM(self):
        vals = self.stage_dict.values()
        return Counter(vals)["REM"]

    def _calc_WAKE(self):
        return (np.sum(self.stage_array[:]=="WAKE") / len(self.stage_array)) * (self.record_len_in_sec / 3600)

    def _calc_N_WAKE(self):
        vals = self.stage_dict.values()
        return Counter(vals)["WAKE"]

    def _calc_NREM(self):
        return (np.sum(self.stage_array[:]=="NREM") / np.sum(self.stage_array != "WAKE")) * self._calc_TST()

    def _count_Pose(self):
        vals, counts = np.unique(self.poses[self.stage_array != "WAKE"], return_counts=True)

        return (np.max(counts) / np.sum(self.stage_array != "WAKE")) * self._calc_TST()

    def get_sleeping_score(self):
        if np.min(np.asarray(self.stage_array) == "WAKE"):
            results = dict()

            parameters = dict()
            parameters["TST"] = 0
            parameters["TR"] = 0
            parameters["TW"] = 0
            parameters["TNR"] = 0
            parameters["A"] = 1
            parameters["NR"] = 0
            parameters["P"] = 0

            results["parameters"] = parameters

            scores = dict()
            scores["sc1"] = 0
            scores["sc2"] = 0
            scores["sc3"] = 0

            results["scores"] = scores

            results["stages"] = self.stage_dict

            return results


        TST = self._calc_TST()
        TR = self._calc_REM()
        TW = self._calc_WAKE()
        TNR = self._calc_NREM()
        A = self._calc_N_WAKE()-1
        NR = self._calc_N_REM()
        P = self._count_Pose() # most_frequent_pose

        a_val = (self.config.Am/self.config.Ap)**2
        scores1 = (TST*a_val + TNR*a_val*0.5 + TR*a_val*0.5 - TW*a_val*0.5 - A/self.config.Aw)*self.config.Ap

        scores2 = (NR+A)/TST

        scores3 = (TNR/TST)*self.config.alpha + 100*self.config.beta + P*self.config.gamma

        results = dict()

        parameters = dict()
        parameters["TST"] = TST
        parameters["TR"] = TR
        parameters["TW"] = TW
        parameters["TNR"] = TNR
        parameters["A"] = A
        parameters["NR"] = NR
        parameters["P"] = P

        results["parameters"] = parameters

        scores = dict()
        scores["sc1"] = scores1
        scores["sc2"] = scores2
        scores["sc3"] = scores3

        results["scores"] = scores

        results["stages"] = self.stage_dict

        return results