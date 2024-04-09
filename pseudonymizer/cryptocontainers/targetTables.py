from pseudonymizer.cryptocontainers.bundleTables import BundleTables
from pseudonymizer.cryptocontainers.initTables import InitTables


class TargetTables(BundleTables):
    """결합대상정보 생성 테이블 저장 클래스"""
    init_tables = []
    target_tables = []
    key_columns = None
    serial_cols = []
    target_columns = None

    @classmethod
    def addInitTables(cls, tables: InitTables):
        """원본테이블, 결합키 생성 테이블, 결합대상정보 테이블로 이루어진 InitTables 클래스 받기"""
        cls.init_tables.append(tables)

    @classmethod
    def addKeyColumns(cls, key_columns: list):
        """결합키 생성 항목 컬럼명 입력 메서드"""
        cls.key_columns = key_columns

    @classmethod
    def addTargetColumns(cls, target_columns: list):
        """결합대상정보 컬럼명 입력 메서드"""
        cls.target_columns = target_columns


    @classmethod
    def selectTables(cls):
        """InitTables에서 target_table만 골라내어 저장하기"""
        for table in cls.init_tables:
            cls.target_tables.append(table.target_table)
            cls.serial_cols.append(table.serial_col)


    @classmethod
    def getTableList(cls):
        """결합대상정보 생성 테이블 출력"""
        return cls.target_tables
    
    @classmethod
    def getSchemas(cls):
        """스키마명만 모아서 출력"""
        schemas = []
        for table in cls.target_tables:
            schemas.append(table.getSchema())

        return schemas
    
    @classmethod
    def getTables(cls):
        """테이블명만 모아서 출력"""
        tables = []
        for table in cls.target_tables:
            tables.append(table.getTable())
        
        return tables

    @classmethod
    def reset(cls):
        cls.init_tables = []
        cls.target_tables = []
        cls.key_columns = None
        cls.serial_cols = []
        cls.target_columns = None