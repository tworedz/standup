class WarmUpSummonService:
    @classmethod
    def is_valid_summoner(cls, summoner: str) -> bool:
        usr_string = "$me"
        return usr_string in summoner
