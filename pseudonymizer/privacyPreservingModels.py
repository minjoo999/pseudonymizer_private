from pseudonymizer.deidentificationTechnique.equivalentClass import EquivalentClass
from pseudonymizer.deidentificationTechnique.kAnonymity import K_Anonymity
from pseudonymizer.deidentificationTechnique.lDiversity import L_Diversity
from pseudonymizer.deidentificationTechnique.tClosenessFactor import T_Closeness_F
from pseudonymizer.deidentificationTechnique.tClosenessNumeric import T_Closeness_N
from pseudonymizer.deidentificationTechnique.differentialPrivacy import DifferentialPrivacy
from pseudonymizer.deidentificationTechnique.gaussiandifferentialPrivacy import GaussianDifferentialPrivacy
from typing import *


class PrivacyPreservingModel:
    """개인식별가능정보 속성을 기준으로 그룹화된 데이터로 프라이버시 보호 모델을 적용하여 정량적인 위험성을 규정하는 실행 클래스"""
    def __init__(self, dataframe, epsilon):
        self._dataframe = dataframe
        self.equivalnt_class = EquivalentClass(self._dataframe)
        self.Kanonymity = K_Anonymity(self._dataframe)
        self.Ldiversity = L_Diversity(self._dataframe)
        self.TclosenessNum = T_Closeness_N(self._dataframe)
        self.TclosenessFac = T_Closeness_F(self._dataframe)
        self.LaplaceLDP = DifferentialPrivacy(self._dataframe, epsilon)
        self.GaussianLDP = GaussianDifferentialPrivacy(self._dataframe, epsilon)

    def applyKAnonymityOrLDiversity(self, method: str, K: int, L: int, attributes: List[str], sensitive_attribute):
        """K-익명성과 L-다양성 모델을 선택적으로 적용하는 메서드
        input
        -----
        method: 프라이버시 보호 모델 메서드를 받고, 
        keyword arguments에 딕셔너리 형식으로 각 기법에 필요한 파라미터를 받아옴"""
        if method == "K":
            self.Kanonymity.applyKAnonymity(K, attributes)
                # Kanonymity Input | K: int, attributes: List[str]
            return self.Kanonymity.K_data
        elif method == "L":
            self.Ldiversity.applyLDiversity(K, L, attributes, sensitive_attribute)
                # Ldiversity Input | K: int, L: int, attribute: List[str], sensitive_attribute
            return self.Ldiversity.L_data
        else:
            raise ValueError(f"입력받은 {method}는 유효한 개인정보 보호 기법이 아닙니다.")
        
    def applyLocalLDiversity(self, K: int, L: int, attributes: List[str], sensitive_attribute: str, LocalL: int):
        self.Ldiversity.applyLDiversity(K, L, attributes, sensitive_attribute)
            # Ldiversity Input | K: int, L: int, attribute: List[str], sensitive_attribute
        self.Ldiversity.applyLocalLDiversity(LocalL)
            # LocalLdiversity | local_L: int
        return self.Ldiversity.LocalL_data

    def applyTCloseness(self, method, quasi_identifiers, sensitive_attribute: str, tolerance: float):
        if method == "Numeric":
            self.TclosenessNum.applyTCloseness(quasi_identifiers, tolerance, sensitive_attribute)
            return self.TclosenessNum.T_data
        elif method == "Factor":
            self.TclosenessFac.applyTCloseness(quasi_identifiers, tolerance, sensitive_attribute)
            return self.TclosenessFac.T_data
        else:
            raise ValueError(f"입력받은 {method}는 유효한 t-근접성 기법 적용 자료형이 아닙니다.")
            
    def applyDPrivacy(self, method, boundary, attributes, sensitive_attribute, outlier):
        """차분 프라이버시 기법(차등적 정보보호 기능)을 적용하는 메서드"""
        if method == "Laplace":
            self.LaplaceLDP.dataDeviatingfromCI(boundary, attributes, sensitive_attribute)
            self.LaplaceLDP.dataGlobalSensitivity(outlier)
            return self.LaplaceLDP._dataframe
        elif method == "Gaussian":
            self.GaussianLDP.dataDeviatingfromCI(boundary, attributes, sensitive_attribute)
            self.GaussianLDP.dataGlobalSensitivity(outlier)
            return self.GaussianLDP._dataframe
        else:
            raise ValueError(f"입력받은 {method}는 유효한 차분 프라이버시 보호 기법 적용 확률분포가 아닙니다.")
                
    def __str__(self):
        """동질집합에 대한 정보를 문자열로 반환하는 메서드"""
        return str(self.equivalent_class)