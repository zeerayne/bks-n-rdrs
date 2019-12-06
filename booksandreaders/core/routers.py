import logging
import random
from django.conf import settings
from django.core.cache import caches
from django.db import (connections, DEFAULT_DB_ALIAS)
from django.db.utils import OperationalError


log = logging.getLogger(__name__)


class LoadBalanceRouter(object):

    def __init__(self):
        log.debug('LoadBalanceRouter init')
        self.offline_db_cache = caches[settings.DATABASE_ROUTER_CACHE_KEY]
        self.master_db_alias = DEFAULT_DB_ALIAS
        try:
            self.slave_db_alias = next(filter(lambda alias: alias != self.master_db_alias, settings.DATABASES.keys()))
        except StopIteration:
            self.slave_db_alias = self.master_db_alias
        self.db_aliases = [self.master_db_alias, self.slave_db_alias]

    def db_is_online(self, db_alias, use_cache=True):
        if use_cache and self.offline_db_cache.get(db_alias):
            log.debug(f'DB is offline: {db_alias} /// From cache')
            return False
        log.debug(f'Checking database connection to: {db_alias}')
        try:
            with connections[db_alias].cursor():
                pass
        except OperationalError:
            log.debug(f'DB is offline: {db_alias}')
            self.offline_db_cache.set(db_alias, 'db_offline')
            return False
        else:
            return True

    def db_for_read(self, *args, **kwargs):
        db_aliases = random.sample(self.db_aliases, k=len(self.db_aliases))
        for db_for_read in db_aliases:
            if self.db_is_online(db_for_read):
                log.debug(f'Read DB choice: {db_for_read}')
                return db_for_read
        # If there is no databases online, attempting no-cache checks
        for db_for_read in db_aliases:
            if self.db_is_online(db_for_read, use_cache=False):
                log.debug(f'Read DB choice: {db_for_read} /// WO cache')
                return db_for_read
        raise ValueError('All databases are offline')

    def db_for_write(self, *args, **kwargs):
        db_for_write = self.master_db_alias
        return db_for_write

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db in self.db_aliases and obj2._state.db in self.db_aliases:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == self.master_db_alias:
            return True
        return False
