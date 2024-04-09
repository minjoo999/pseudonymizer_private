from pseudonymizer.cryptocontainers.tableContainer import TableContainer
from pseudonymizer.cryptocontainers.targetTables import TargetTables
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery


class JoinTargetData(PyMySQLQuery):
    """매핑테이블의 일련번호를 기준으로 결합대상정보를 결합하는 클래스"""
    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        super().__init__(pw = pw)
        super().connectDatabase(serverIP, port_num, user_name, database_name, kr_encoder)

        self.target_tables = None
        self.mapping_table = None
        self.result = None

    def addTargetTables(self, target_tables: TargetTables):
        """결합대상정보 테이블 객체 입력"""
        self.target_tables = target_tables

    def addMappingTable(self, mapping_table: TableContainer):
        """매핑테이블 스키마, 테이블 이름 입력"""
        self.mapping_table = mapping_table

    def addResult(self, result: TableContainer):
        """결합대상정보 결합 클래스 내용 주입"""
        self.result = result

    def joinDB(self):
        """매핑테이블의 일련번호를 기준으로 결합대상정보를 결합하는 메서드
           결합키를 제외한 컬럼명들을 SELECT에 나열하고, INNER JOIN을 한줄씩 더하기
        """
        schemas = self.target_tables.getSchemas()
        tables = self.target_tables.getTables()

        serial_cols = self.target_tables.serial_cols
        target_cols = ', '.join(self.target_tables.target_columns)

        mapping_schema = self.mapping_table.getSchema()
        mapping_table = self.mapping_table.getTable()
        result_schema = self.result.getSchema()
        result_table = self.result.getTable()

        create_sql = f"CREATE TABLE {result_schema}.{result_table} AS "
        select_sql = f"SELECT {mapping_schema}.{mapping_table}.*, {target_cols} "
        from_sql = f"FROM {mapping_schema}.{mapping_table} "
        join_sql = f""

        for i in range(len(tables)):
            join_sql += f"INNER JOIN {schemas[i]}.{tables[i]} ON {schemas[i]}.{tables[i]}.{serial_cols[i]} = {mapping_table}.{serial_cols[i]} "
            
        sql = create_sql + select_sql + from_sql + join_sql

        super().dataQueryLanguage(sql)
        super().executeQuery()