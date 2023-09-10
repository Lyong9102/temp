from typing import Tuple,List
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd   
from pandas import Series,DataFrame

from load_simulation_core_sdk.algorithm.base import BaseTimeseriesCalculator
from load_simulation_data_sdk.timeseries.meta_data.channel_entity import ChannelInfo
from load_simulation_core_sdk.algorithm.base_meta_data import AlgorithmSimData


class TimeseriesCalculator(BaseTimeseriesCalculator):
    def __init__(self, sim_data: AlgorithmSimData, channels_info: list[ChannelInfo]):
        super().__init__(sim_data, channels_info)

    def _do_calculation(self,flag)-> Tuple[pd.DataFrame, List[pd.DataFrame]]:
        if flag:
            print("Split Timeseries")
        if len(self.sim_data.dlcs) == 1:
            dlc = self.sim_data.dlcs[0]
            cases = dlc.all_cases_channel_timeseries
            case_list = []
            df_cases_summary = pd.DataFrame()
            for case in cases:
                # 在这里，你可以对每个 case 进行你需要的操作
                file_name = f"{case.dlc_name[3:6]}_{case.name}.txt"
                safety_factor = case.safety_factor
                step = case.channels_timeseries[0].step
                lens = len(case.channels_timeseries[0].timeseries)

                # 生成时序数据文件的摘要信息,输出到摘要报告
                d = {"FileName": file_name,
                    # "Frequency": f"Frequency{occurrence_during_lifetime}",
                    "Frequency": "Frequency",
                    "Time Discretisation": step,
                    "Number of time steps": lens,
                    "Safety factor": '1.0', # 固定值1.0
                    "Operating Status": "operating_status",# 仅yaml
                    }
                case_list.append(d)

                # 计算每个case的时序数据
                start = case.channels_timeseries[0].start
                Time = pd.Series([start + step * i for i in range(lens)], name="Time [s]").round(3)
                datas = [(pd.Series(col.timeseries, name=f"{col.name}{col.orig_unit[:1] + 'k' + col.orig_unit[1:]}") / 1000).round(3) for col
                        in case.channels_timeseries]
                datas.append(Time)
                df = pd.concat(datas, axis=1)
                # 创建新的列顺序列表
                first_col = "Time [s]"
                other_cols = sorted((col for col in df.columns if col != first_col), reverse=False)
                new_order = [first_col] + other_cols
                # 使用reindex方法设置新的列顺序
                df = df.reindex(new_order, axis=1)
                # 输出时序数据report_data 为csv文件,命名为txt
                data_frame = []
                data_frame.append(df.columns.tolist())
                for data in df.values.tolist():
                    data_frame.append(data)
                
        return df_cases_summary,df_cases_list

    def _do_calculation_concurrency(self):
        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(self._process_dlc, dlc): dlc for dlc in self.sim_data.dlcs}
            dlcs_list = []
            for future in as_completed(futures):
                dlcs_list.append(future.result())
        return dlcs_list

    def _process_dlc(self, dlc):
        # 在这里，你可以对每个dlc进行你需要的操作
        return dlc

    def _check_data_validation(self):
        if len(self.sim_data.dlcs) == 0:
            raise ValueError(f'no dlc data in sim_data, sim: {self.sim_data.sims}')
