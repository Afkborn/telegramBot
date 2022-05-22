class User:
    def __init__(self, 
                id : int = None,
                telegram_id : int = None,
                is_bot : bool = None,
                username : str = None,
                first_name : str = None,
                last_name : str = None,
                language_code : str = None,
                created_at : int = None,
                ):
        self.__id = id
        self.__telegram_id = telegram_id
        self.__is_bot = is_bot
        self.__username = username
        self.__first_name = first_name
        self.__last_name = last_name
        self.__language_code = language_code
        self.__created_at = created_at
        
    def get_id(self) -> int:
        return self.__id
    
    def get_telegram_id(self) -> int:
        return self.__telegram_id
    
    def get_is_bot(self) -> bool:
        return self.__is_bot
    
    def get_username(self) -> str:
        return self.__username
    
    def get_first_name(self) -> str:
        return self.__first_name
    
    def get_last_name(self) -> str:
        return self.__last_name
    
    def get_language_code(self) -> str:
        return self.__language_code
    
    def get_created_at(self) -> int:
        return self.__created_at
    
    def set_id(self, id):
        self.__id = id
        
    def set_telegram_id(self, telegram_id : int) -> int:
        self.__telegram_id = telegram_id
        return self.__telegram_id
        
    def set_is_bot(self, is_bot : bool) -> bool:
        self.__is_bot = is_bot
        return self.__is_bot
        
    def set_username(self, username : str) -> str:
        self.__username = username
        return self.__username
        
    def set_first_name(self, first_name :   str):
        self.__first_name = first_name
        return self.__first_name
        
    def set_last_name(self, last_name : str) -> str:
        self.__last_name = last_name
        return self.__last_name
        
    def set_language_code(self, language_code: str) -> str:
        self.__language_code = language_code
        return self.__language_code
    
    def set_created_at(self, created_at : int) -> int:
        self.__created_at = created_at
        return self.__created_at
        
        

