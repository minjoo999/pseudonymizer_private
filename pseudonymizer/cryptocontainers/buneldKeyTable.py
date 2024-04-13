from pseudonymizer.cryptocontainers.DBContainer import DBContainer
from pseudonymizer.cryptocontainers.bundleTables import BundleTables


class BundleKeyTable(BundleTables):
    """결합키 생성 테이블 저장 상속 클래스"""
    dbtables = None
    key_column = None

    def __init__(self):
        self.key_table = None

    @classmethod
    def addDBTables(cls, tables: DBContainer):
        """DB에서 가명결합을 수행할 원본 테이블 캡슐화하는 메서드"""
        cls.dbtables = tables
    
    @classmethod
    def addKeyColumn(cls, key_column: str):
        """일방향 암호화 수행대상 결합키 컬럼명 설정하는 메서드"""
        cls.key_column = key_column

    def selectTables(self, key_table: DBContainer):
        """결합키 생성에 활용될 테이블 저장하는 클래스"""
        self.key_table = key_table

    def getTableList(self):
        """결합키 생성항목 테이블 반환하는 메서드"""
        return self.key_table

    def getSchemas(self):
        """스키마명 반환하는 메서드"""
        return self.key_table.getSchema()

    def getTables(self):
        """테이블명 반환하는 메서드"""
        return self.key_table.getTable()

    @classmethod
    def reset(cls):
        """클래스 변수 초기화"""
        cls.dbtables = None
        cls.key_column = None
