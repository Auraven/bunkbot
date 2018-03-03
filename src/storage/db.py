"""
Wrapper for the TinyDB database storage
with helper methods and additional functions
"""
import discord, datetime, pytz
from tinydb import TinyDB, Query
from tinydb.database import Table
from src.util.functions import to_name

CONFIG = Query()
USERS = Query()
RPG = Query()

class BunkDB:
    # establish a 'connection' to the local
    # database and read in the primary tables
    def __init__(self):
        self.db = TinyDB("src/storage/db.json")
        self.config: Table = self.db.table("config")
        self.users: Table = self.db.table("users")
        self.rpg: Table = self.db.table("rpg")
        self.holiday: Table = self.db.table("holiday")
        self.streams: Table = self.db.table("streams")
        self.check_defaults()


    # set default database and config values
    def check_defaults(self):
        if len(self.config.all()) == 0:
            self.config.insert_multiple([
                {"token": ""},
                {"serverid": ""},
                {"cleverbot": ""},
                {"weather": ""},
                {"twitch_id": ""},
                {"twitch_secret": ""}
            ])

        if len(self.rpg.all()) == 0:
            self.rpg.insert_multiple([{"xp_const": 5}, {"update_cap": 60}, {"timer_minutes": 1}])


    # helper method that will query the requested table
    # and property name - default table as config
    def get(self, attr: str) -> str or None:
        res = self.config.get(CONFIG[attr] != "")
        if res is not None:
            return res[attr]
        else:
            return None


    # get a user based on the passed
    # discord member name reference
    def get_user_by_name(self, name: str) -> any:
         return self.users.get(Query().name == to_name(name))


    # get a user based on the passed
    # discord member id reference
    def get_user_by_id(self, id: str) -> any:
         return self.users.get(Query().id == id)


    # check if a user exists in the database - if not,
    # add them with base roles and properties
    def check_user_with_member(self, member: discord.Member) -> bool:
        user: Table = self.users.search(Query().name == to_name(member.name))

        if len(user) == 0:
            self.users.insert({"name": to_name(member.name), "id": member.id, "member_name": member.name, "xp": 0, "level": 1})
            if not str(member.status) == "offline":
                self.update_user_last_online(to_name(member.name))
            return True

        if not str(member.status) == "offline":
            self.update_user_last_online(to_name(member.name))
        return False


    # update the "last online" property for
    # a user when a user appears online
    def update_user_last_online(self, name: str) -> None:
        now = datetime.datetime.now(tz=pytz.timezone("US/Eastern"))
        last_on = "{0:%m/%d/%Y %I:%M:%S %p}".format(now)
        self.users.update({"last_online": last_on}, Query().name == to_name(name))


    # update the users level percentage
    # and return the user reference
    def update_user_xp(self, name: str, value: float) -> any:
        user = self.get_user_by_name(name)
        cur_xp = float(user["xp"])

        new_xp = 0
        if cur_xp + value > 0:
            new_xp = round(cur_xp + value, 2)

        now = datetime.datetime.now()
        last_xp = "{0:%m/%d/%Y}".format(now)

        self.users.update({"xp": new_xp, "last_xp_updated": last_xp}, Query().name == to_name(name))

        user = self.get_user_by_name(name)
        return user


    # update the users level
    # and return the user reference
    def update_user_level(self, name: str, value: int = 1) -> any:
        user = self.get_user_by_name(name)
        cur_lvl = int(user["level"])

        self.users.update({"level": cur_lvl + value}, Query().name == to_name(name))

        user = self.get_user_by_name(name)
        return user


database: BunkDB = BunkDB()
