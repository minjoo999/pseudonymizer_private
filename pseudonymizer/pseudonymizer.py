# ./pseudonymizer/pseudonymizer.py

from abc import ABC, ABCMeta, abstractmethod
from typing import List
import pandas as pd

class Pseudonymizer(ABC):
    """가명처리 추상 클래스 및 추상 메서드 선언"""
    @abstractmethod
    def pseudonymizeData(self, value):
        """확장성을 갖춘 가명처리 클래스를 만들어 특정 가명처리 기법으로 구체화하기 위한 추상 메서드"""
        pass