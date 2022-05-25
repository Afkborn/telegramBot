from urllib.parse import urlparse

class Product:
    def __init__(self,
    id:int=None, # id
    owner_telegram_id : int = None, # owner_telegram_id
    isim:str=None, #ürün ismi
    link:str=None, # ürün linki
    fiyat_takip:bool=None, #fiyat takip
    stok_takip:bool=None, #stok takip
    fiyat:float=None,  #ürün fiyatı
    stok:bool=None, #stok durumu
    son_kontrol_zamani:float=None, #son kontrol zamanı
    created_at:float=None, #oluşturulma zamanı
    birim_id:int=None, #birim id
    ) -> None:
        
        self.__id = id
        self.__owner_telegram_id = owner_telegram_id
        self.__isim = isim
        self.__link = link
        self.__fiyat_takip = fiyat_takip
        self.__stok_takip = stok_takip
        self.__fiyat = fiyat
        self.__stok = int(stok)
        self.__son_kontrol_zamani = son_kontrol_zamani
        self.__created_at = created_at
        self.__birim_id = birim_id
        

    def get_id(self):
        return self.__id 
    def get_owner_telegram_id(self):
        return self.__owner_telegram_id
    def get_isim(self):
        return self.__isim
    def get_link(self):
        return self.__link
    def get_fiyat_takip(self):
        if (self.__fiyat_takip):
            return 1
        return 0
    def get_stok_takip(self):
        if (self.__stok_takip):
            return 1
        return 0
    def get_fiyat(self):
        return self.__fiyat
    def get_stok(self):
        if (self.__stok):
            return 1
        return 0
    def get_stok_string(self):
        if (self.__stok):
            return "✅"
        return "❌"
    def get_son_kontrol_zamani(self):
        return self.__son_kontrol_zamani
    def get_created_at(self):
        return self.__created_at
    def get_type(self):
        if (self.__fiyat_takip and self.__stok_takip):
            return "Stock and Price"
        elif (self.__fiyat_takip):
            return "Price"
        else:
            return "Stock"
    def get_domain(self):
        return ".".join(urlparse(self.get_link()).netloc.split('.')[0:])
    def get_birim_id(self) -> int:
        return self.__birim_id
        

    def set_id(self,id):
        self.__id = id
    def set_owner_telegram_id(self,owner_telegram_id):
        self.__owner_telegram_id = owner_telegram_id
    def set_isim(self,isim):
        self.__isim = isim
    def set_link(self,link):
        self.__link = link
    def set_fiyat_takip(self,fiyat_takip):
        self.__fiyat_takip = fiyat_takip
    def set_stok_takip(self,stok_takip):
        self.__stok_takip = stok_takip
    def set_fiyat(self,fiyat : int):
        self.__fiyat = fiyat
    def set_stok(self,stok):
        self.__stok = stok
    def set_son_kontrol_zamani(self,son_kontrol_zamani):
        self.__son_kontrol_zamani = son_kontrol_zamani
    def set_created_at(self,created_at):
        self.__created_at = created_at
    def set_birim_id(self,birim_id : int):
        self.__birim_id = birim_id
        
        
    def __str__(self) -> str:
        return "Product: id={}, owner_telegram_id={}, isim={}, link={}, fiyat_takip={}, stok_takip={}, fiyat={}, stok={}, son_kontrol_zamani={}, created_at={}".format(
            self.__id,
            self.__owner_telegram_id,
            self.__isim,
            self.__link,
            self.__fiyat_takip,
            self.__stok_takip,
            self.__fiyat,
            self.__stok,
            self.__son_kontrol_zamani,
            self.__created_at,
        )



        
