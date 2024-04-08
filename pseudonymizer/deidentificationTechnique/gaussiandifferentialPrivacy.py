from pseudonymizer.deidentificationTechnique.equivalentClass import EquivalentClass
from typing import *
from scipy.stats import norm
from math import exp, pi


class GaussianDifferentialPrivacy(EquivalentClass):
    """가우시안 메커니즘 적용 차분 프라이버시 클래스"""
    def __init__(self, dataframe, ratio_bounded):
        # 개별 동질집합 속성값을 키로 가지고 인덱스 번호를 값으로 가지는 딕셔너리
        super().__init__(dataframe)
        # 신뢰구간을 초과하는 키와 값만 저장한 딕셔너리
        self.upperoutlier_dictionary = {}
        self.loweroutlier_dictionary = {}
        self.sensitive_attribute = None
        # epsilon으로 개인정보(가명정보) 보호 수준을 결정하는 하이퍼 파라미터
        self.ratio_bounded = ratio_bounded
    
    def dataDeviatingfromNormCI(self, boundary: float, attributes: List[str], sensitive_attribute: str):
        """동질집합 내 평균에서 양쪽 3표준편차(예: 3시그마)의 범위 99.7%에 들지 않는 민감정보 행 번호만 별도로 추출하는 메서드
        가설검정 기반에서 노이즈를 입력하는 방식인 GDP(Gaussian Differential Privacy) 방법
        이 방식은 통계 가설 관점에서 주어진 유의 수준에서 최소의 제2종 오류를 trade-off function으로 나타냄으로써 차분 정보보호 적용"""
        super().categorizeEquivalentClass(attributes)
        self.sensitive_attribute = sensitive_attribute
        for group_key, index_value in self.equivalent_class.items():
            mu = np.nanmean(self._dataframe.loc[index_value, sensitive_attribute])
            sigma = np.nanstd(self._dataframe.loc[index_value, sensitive_attribute])

            for i in index_value:
                x = self._dataframe.loc[i, self.sensitive_attribute]
                if mu-boundary*sigma <= x <= mu+boundary*sigma:
                    pass
                elif x > mu+boundary*sigma:
                    self.upperoutlier_dictionary.setdefault(group_key, []).append(i)
                elif x < mu-boundary*sigma:
                    self.loweroutlier_dictionary.setdefault(group_key, []).append(i)
                else:
                    raise ValueError(f"{x}은 유효한 수가 아닙니다.")
    
    def dataNormGlobalSensitivity(self, outlier):
        """특정 레코드(식별가능한 개인) 유무에 따른 민감도를 산출하는 메서드
        특정 결과를 얻기 위한 쿼리 K를 각 데이터에 적용한 결과인 K(D1)와 K(D2)가 동일한 분포 S에 속할
        확률의 비율(두 데이터 분포의 차이)을 일정 수준(epsilon)보다 작도록 함"""
        col_num = self._dataframe.columns.get_loc(self.sensitive_attribute)
        
        if outlier == "upper":
            for group_key, outlier_list in self.upperoutlier_dictionary.items():
                
                for i in outlier_list:
                    upper_outlier = self._dataframe.iloc[i, col_num]
                    group_data, exception_data = 0, 0
                    
                    group_list = self.equivalent_class[group_key]
                    group_data = self._dataframe.iloc[group_list, col_num]
                    group_list.remove(i)
                    exception_list = group_list[:]
                    exception_data = self._dataframe.iloc[exception_list, col_num]
                    
                    pseudonymize_data = self.gaussianMechanism(
                        group_data, exception_data, upper_outlier, outlier)
                    print(i, upper_outlier, pseudonymize_data)
                    self._dataframe.loc[i, self.sensitive_attribute] = pseudonymize_data
        
        elif outlier == "lower":
            for group_key, outlier_list in self.loweroutlier_dictionary.items():
                for i in outlier_list:
                    lower_outlier = self._dataframe.iloc[i, col_num]
                    group_data, exception_data = 0, 0
                    
                    group_list = self.equivalent_class[group_key]
                    group_data = self._dataframe.iloc[group_list, col_num]
                    
                    group_list = self.equivalent_class[group_key]
                    group_data = self._dataframe.iloc[group_list, col_num]
                    group_list.remove(i)
                    exception_list = group_list[:]
                    exception_data = self._dataframe.iloc[exception_list, col_num]
                    
                    pseudonymize_data = self.gaussianMechanism(
                        group_data, exception_data, lower_outlier, outlier)
                    print(i, lower_outlier, pseudonymize_data)
                    self._dataframe.loc[i, self.sensitive_attribute] = pseudonymize_data                    
    
    @classmethod
    def estimateGaussianParameters(cls, data):
        """정규분포의 모수 평균(mu)과 표준편차(sigma)를 추정하는 메서드"""
        mu = np.nanmean(data)
        sigma = np.nanstd(data)
        return mu, sigma
    
    @classmethod
    def gaussianPDF(cls, x, mu, sigma):
        """정규분포(가우시안) 확률밀도함수(확률변수가 특정한 값을 가질 확률을 나타내는 함수)"""
        return (1/np.sqrt(2*pi*sigma**2)) * np.exp(-0.5*((x-mu)/sigma)**2)
    
    @classmethod
    def calculateNormProbabilityRatio(cls, include_data, exclude_data):
        """확률변수 X가 정규분포에 속할 확률과 특정 행의 포함 여부 데이터 간 비율을 계산하는 메서드"""
        # 두 데이터의 평균과 표준편차 파라미터를 추정
        mu_include, sigma_include = cls.estimateGaussianParameters(include_data)
        mu_exclude, sigma_exclude = cls.estimateGaussianParameters(exclude_data)

        # 두 데이터의 정규분포에 속할 확률 계산
        prob_include = cls.gaussianPDF(include_data, mu_include, sigma_include)
        prob_exclude = cls.gaussianPDF(exclude_data, mu_exclude, sigma_exclude)
        prob_ratio = prob_include / prob_exclude

        # 두 데이터의 정규분포에 속할 확률의 비율 계산
        return prob_ratio
    
    def gaussianMechanism(self, include_data, exclude_data, particular_record, outlier):
        # 전역 민감도 계산
        sensitivity = self.calculateNormProbabilityRatio(include_data, exclude_data)
        # 사용자 지정 개인정보 보호 수준, 하이퍼파라미터 엡실론을 통해 스케일 파라미터 정의 
        beta = sensitivity / self.ratio_bounded
        # 평균 0, 시그마 값을 분산으로 가지는 정규분포에 속하는 랜덤 난수 추출
        noise = np.random.normal(0, beta, len(include_data))
        random_noise = np.random.choice(noise)

        # 이상치에 노이즈 추가
        if outlier == "lower":
            return particular_record + random_noise if random_noise >= 0 else particular_record - random_noise
        elif outlier == "upper":
            return particular_record - random_noise if random_noise >= 0 else particular_record + random_noise
        else:
            raise ValueError(f"{outlier}은 유효한 이상치 유형이 아닙니다.")