from pseudonymizer.encryptionPseudonyms.divideOriginalTable import DivideOriginalTable
from pseudonymizer.encryptionPseudonyms.encryptKeyCol import EncryptKeyCol
from pseudonymizer.encryptionPseudonyms.makeInitTables import MakeInitTables


class DivideEncrypter:
    """DivideOriginalTable 및 EncryptKeyCol 클래스를 통해 분할 및 암호화 진행"""
    def __init__(self):
        self.pw = None
        self.serverIP = None
        self.port_num = None
        self.user_name = None
        self.database_name = None
        self.kr_encoder = None

        self.original_table = None
        self.key_table = None
        self.target_table = None

        self.columns = None
        self.serial_col = None
        self.serial_text = None
        self.join_key = None

    def addDBInfo(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        """DB 연결 정보 입력"""
        self.pw = pw
        self.serverIP = serverIP
        self.port_num = port_num
        self.user_name = user_name
        self.database_name = database_name
        self.kr_encoder = kr_encoder
    
    def addTablesInfo(self, original_table: tuple, key_table: tuple, target_table: tuple):
        """InitTables 생성 정보 입력 메서드"""
        self.original_table = original_table
        self.key_table = key_table
        self.target_table = target_table

    def addSerialKeyInfo(self, columns: list, serial_col: str, serial_text: str, join_key: str):
        """결합키 및 일련번호 컬럼 입력 메서드"""
        self.columns = columns
        self.serial_col = serial_col
        self.serial_text = serial_text
        self.join_key = join_key
    
    def makeInitTables(self):
        """InitTables 생성 메서드"""
        init_tables = MakeInitTables(self.original_table, self.key_table, self.target_table).makeInitTables(self.columns, self.serial_col, self.serial_text, self.join_key)
        return init_tables

    def divideOriginalTable(self, salt: str):
        """InitTables 클래스를 통해 테이블 분할 메서드"""
        init_tables = self.makeInitTables()
        divide_table = DivideOriginalTable(self.pw, self.serverIP, self.port_num, self.user_name, self.database_name, self.kr_encoder)

        divide_table.addInitTables(init_tables=init_tables)
        divide_table.addSerialNum()
        divide_table.insertKey(salt)
        divide_table.insertTarget()

    def encryptKeyCol(self, func: str):
        """EncryptKeyCol 클래스를 통해 결합키 암호화"""
        init_tables = self.makeInitTables()
        encrypt_key = EncryptKeyCol(self.pw, self.serverIP, self.port_num, self.user_name, self.database_name, self.kr_encoder)
        encrypt_key.addInitTables(init_tables)
        encrypt_key.encryptKeyCol(func)
    