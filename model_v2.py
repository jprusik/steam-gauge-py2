from elixir import metadata, Float, Text, Unicode, UnicodeText, DateTime, String, Integer, Boolean, Entity, Field, using_options, setup_all, session, PickleType
import datetime
import config

metadata.bind = config.MYSQL_DATABASE_URI
metadata.bind.echo = False

class App(Entity):
    using_options(tablename='APPS')
    achievements_enabled = Field(Boolean)
    app_id = Field(Unicode(20), primary_key=True)
    app_title = Field(UnicodeText)
    app_type = Field(UnicodeText)
    app_website = Field(UnicodeText)
    big_logo = Field(UnicodeText)
    big_picture_api_raw = Field(Text)
    captions = Field(Boolean)
    commentary = Field(Boolean)
    controller_support = Field(UnicodeText)
    hdr = Field(Boolean)
    hours_played = Field(Float)
    icon = Field(UnicodeText)
    last_updated = Field(DateTime)
    leaderboards_enabled = Field(Boolean)
    metascore = Field(UnicodeText)
    metascore_link = Field(UnicodeText)
    minutes_played = Field(Integer)
    multiplayer = Field(Boolean)
    os_linux = Field(Boolean)
    os_mac = Field(Boolean)
    os_windows = Field(Boolean)
    release_date = Field(UnicodeText)
    required_age = Field(Integer)
    singleplayer = Field(Boolean)
    size_mb = Field(Float)
    small_logo = Field(UnicodeText)
    source_sdk_included = Field(Boolean)
    stats_enabled = Field(Boolean)
    steamcloud_enabled = Field(Boolean)
    store_price_default_usd = Field(Float)
    tradingcards_enabled = Field(Boolean)
    VAC_enabled = Field(Boolean)
    workshop_enabled = Field(Boolean)

    # def __repr__(self):
    #     return '<App %s - "%s" (%s%s) | Type: %s | Multi: %s | Price: $%s | Windows: %s | Mac: %s | Linux: %s | Joy: %s | Metacritic: %s | %s | %s | %s>' % (self.appid, self.title, self.hdspace, self.hdunit, self.apptype, self.multiplayer, self.usprice, self.win_support, self.mac_support, self.linux_support, self.joysupport, self.metacritic, self.app_icon, self.app_slogo, self.app_logo)

class Genre(Entity):
    using_options(tablename='GENRES')
    name = Field(Unicode(200), primary_key=True)

class Genre_App_Map(Entity):
    using_options(auto_primarykey=True, tablename='GENRE_APP_MAP')
    genres = Field(Unicode(200), index=True)
    apps = Field(Unicode(20), index=True)

class Developer(Entity):
    using_options(tablename='DEVELOPERS')
    name = Field(Unicode(200), primary_key=True)

class Developer_App_Map(Entity):
    using_options(auto_primarykey=True, tablename='DEVELOPER_APP_MAP')
    developers = Field(Unicode(200), index=True)
    apps = Field(Unicode(20), index=True)

class Publisher(Entity):
    using_options(tablename='PUBLISHERS')
    name = Field(Unicode(200), primary_key=True)

class Publisher_App_Map(Entity):
    using_options(auto_primarykey=True, tablename='PUBLISHER_APP_MAP')
    publishers = Field(Unicode(200), index=True)
    apps = Field(Unicode(20), index=True)

class Language(Entity):
    using_options(tablename='LANGUAGES')
    name = Field(Unicode(200), primary_key=True)

class Language_App_Map(Entity):
    using_options(auto_primarykey=True, tablename='LANGUAGE_APP_MAP')
    languages = Field(Unicode(200), index=True)
    apps = Field(Unicode(20), index=True)

class Multiplayer_type(Entity):
    using_options(tablename='MULTIPLAYER_TYPES')
    name = Field(Unicode(200), primary_key=True)

class Multiplayer_type_App_Map(Entity):
    using_options(auto_primarykey=True, tablename='MULTIPLAYER_TYPE_APP_MAP')
    multiplayer_types = Field(Unicode(200), index=True)
    apps = Field(Unicode(20), index=True)

class DLC_id(Entity):
    using_options(tablename='DLC_IDS')
    name = Field(Unicode(200), primary_key=True)

class DLC_id_App_Map(Entity):
    using_options(auto_primarykey=True, tablename='DLC_ID_APP_MAP')
    dlc_ids = Field(Unicode(200), index=True)
    apps = Field(Unicode(20), index=True)

class Users(Entity):
    using_options(auto_primarykey=True, tablename='USERS')
    user_id = Field(Unicode(20), index=True)
    attributes = Field(PickleType)
    last_update = Field(DateTime)
