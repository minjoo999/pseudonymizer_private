from pseudonymizer.cryptocontainers.keyTables import KeyTables
from pseudonymizer.cryptocontainers.tableContainer import TableContainer
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery


class CreateMappingTable(PyMySQLQuery):
    """매핑테이블 만들기 클래스"""
    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        super().__init__(pw = pw)
        super().connectDatabase(serverIP, port_num, user_name, database_name, kr_encoder)

        self.key_tables = None
        self.mapping_table = None
        
    def addKeyTables(self, key_tables: KeyTables):
        """결합키 테이블 객체 입력"""
        self.key_tables = key_tables

    def addMappingTable(self, mapping_table: TableContainer):
        """매핑테이블 스키마, 테이블 이름 입력"""
        self.mapping_table = mapping_table

    def joinDB(self):
        """일련번호를 결합키 기준으로 결합하여 매핑테이블 만드는 메서드"""
        result_schema = self.mapping_table.getSchema()
        result_table = self.mapping_table.getTable()

        schemas = self.key_tables.getSchemas()
        tables = self.key_tables.getTables()
        serial_cols = self.key_tables.getSerialCols()

        super().dataQueryLanguage(f"DROP TABLE IF EXISTS {result_schema}.{result_table}")
        super().executeQuery()

        create_sql = f"CREATE TABLE {result_schema}.{result_table} AS "
        select_sql = f"SELECT {schemas[0]}.{tables[0]}.{self.key_tables.key_col}, {schemas[0]}.{tables[0]}.{serial_cols[0]}, {schemas[1]}.{tables[1]}.{serial_cols[1]}  "
        from_sql = f"FROM {schemas[0]}.{tables[0]} "
        join_sql = f"INNER JOIN {schemas[1]}.{tables[1]} ON {schemas[0]}.{tables[0]}.{self.key_tables.key_col} = {schemas[1]}.{tables[1]}.{self.key_tables.key_col} "

        if len(tables) > 2:
            for i in range(2, len(tables)):
                select_sql += f"{serial_cols[i]}, "
                join_sql += f"INNER JOIN {schemas[i]}.{tables[i]} ON {schemas[0]}.{tables[0]}.{self.key_tables.key_col} = {schemas[i]}.{tables[i]}.{self.key_tables.key_col} "
        else:
            pass

        select_sql = select_sql[:-2] + " "

        sql = create_sql + select_sql + from_sql + join_sql

        super().dataQueryLanguage(sql)
        super().executeQuery()