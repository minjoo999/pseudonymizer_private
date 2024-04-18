import numpy as np
from pseudonymizer.deidentificationTechnique.equivalentClass import EquivalentClass
from typing import *
from scipy.stats import wasserstein_distance

class T_Closeness_N(EquivalentClass):
    """민감 정보(SA)의 분포를 전체 데이터 셋의 분포와 유사하도록 하는 T-근접성 클래스
    
    l-다양성과 달리 민감정보를 원본 그대로 배열에 저장한 후 
    데이터를 내림차순 정렬하여 (확률분포의 차이)
    데이터의 분포도를 측정하는 t-근접성 알고리즘 의사코드
    -----------------------------------------------------
    basic Earth Mover's Distance algorithms
    Input : t_list
    Output : EMD
    """
    def __init__(self, dataframe):
        super().__init__(dataframe)
        self.T_data = None
        self.sensitive_attribute = None
        self.tolerance = None
        
    def checkSensitivesDistribution(self, dataseries):
        """개인식별가능정보(준식별자)의 모든 가능한 조합 n개의 관심 대상값
        (sensitive_attribute)의 분포와 전체 집단의 분포의 거리 최댓값이 <= t로 규정할 때
        분포를 계산하는 메서드"""
        sensitive_vector = dataseries
        cumulative_distribution = {}
        cumulative_probability = 0
        
        # 민감속성의 고유한 값과 그 값의 비율 {v: count/len(V)}
        if sensitive_vector.dtype in ["int64", "float"]:
            # 오름차순 정렬 후 중복값을 제거한 SA를 전체 데이터의 길이로 나눈 값을 확률로 하는 누적분포를 계산 
            ordered_vector = np.sort(sensitive_vector)            
            unique_value, counts = np.unique(ordered_vector, return_counts = True)
            ordered_scalar = np.array(unique_value)
            cumulative_distribution = np.cumsum(counts) / len(sensitive_vector)
    
        elif sensitive_vector.dtype in ["object", "category"]:
            # cumulative_distribution = {v: count/len(v) for (v, count) in Counter(sensitive_vector).items()}
            for value, count in Counter(sensitive_vector).items():
                probability = count / len(sensitive_vector)
                cumulative_probability += probability
                cumulative_distribution[value] = cumulative_probability
        
        else: 
            raise ValueError("입력받은 {}은 유효한 자료형이 아닙니다.".format(dataseries.dtype))
        
        return ordered_scalar, cumulative_distribution

    def earthMoversDistance(self, qi_dist, total_dist):
        """scipy.wasserstein_distance(data_sensitivity, data_population)"""
        # t수치 측정은 EMD(Earth Mover Distance)을 이용하여 계산
        # eucdistance = np.sqrt((qi_dist - total_dist)**2)
        # emdistance = np.sum(np.abs(qi_dist - total_dist))
        emdvalues: List = []

        for qi_p, total_p in zip(qi_dist, total_dist):
            emdvalue = np.sum( np.abs(qi_p - total_p) )
            emdvalues.append(emdvalue)
        emdistance = np.mean(emdvalues)

        return emdistance
    
    def kullbackLeiblerDivergence(self, qi_dist, total_dist):
        """KL발산: 두 확률분포의 평균과 표준편차를 입력으로 받아 계산
        trash code"""
        try:
            return np.sum(qi_dist * np.log(qi_dist / total_dist))
        except ZeroDivisionError as e:
            return 1
            
    def applyTCloseness(self, quasi_identifiers, tolerance: float, sensitive_attribute: str):
        """tolerance: 허용가능한 확률분포 차이의 범위를 정의하여 T-근접성을 적용하는 메서드"""
        T_data = dict()
        qi_distribution, total_distribution = {}, {}

        if tolerance >= 0: 
            # threshold
            super().categorizeEquivalentClass(quasi_identifiers)
            vector = np.array(self._dataframe[sensitive_attribute])
            sorted_total_data, total_distribution = self.checkSensitivesDistribution(vector)

            for group_key, index_value in self.equivalent_class.items():
                # 1. Empirical Cummulative Probability Distribution
                sorted_qi_data, qi_distribution[group_key] = self.checkSensitivesDistribution(vector[index_value])
                sorted_merged_data = np.unique(np.concatenate( (sorted_qi_data, sorted_total_data) ))
                    # np.argsort(): 각 위치별 순서 나타내는 함수 | np.concatenate: 배열끼리 오름차순 병합

                # 2. 두 비대칭 경험누적확률분포의 길이를 맞추기 위한 선형 보간 수행
                qi_ecdf = np.interp(
                    sorted_merged_data, sorted_qi_data, qi_distribution[group_key], left = 0, right = 1)
                total_ecdf = np.interp(
                    sorted_merged_data, sorted_total_data, total_distribution, left = 0, right = 1) 

                # 3. Earth's Mover Distance
                emd = self.earthMoversDistance(qi_ecdf, total_ecdf)
                # 3. KL Divergence
                # kld = self.kullbackLeiblerDivergence(qi_ecdf, total_ecdf)

                # 4.
                if emd < tolerance:
                    # if kld < tolerance:
                    print("T-근접성 성립하는 동질집합:", group_key, emd, "\n", len(index_value), "\n")
                    T_data[group_key] = index_value
                else:
                    print("T-근접성에서 이탈한 동질집합:", group_key, emd, "\n", len(index_value), "\n")
                    pass
                self.T_data = T_data
                
        else: 
            raise ValueError("입력받은 {}은 허용가능한 동질집합과 전체집단 간 확률분포 차이의 범위로서 유효하지 않습니다.".format(tolerance))