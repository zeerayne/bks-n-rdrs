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
        self.MASTER_DB_ALIAS = DEFAULT_DB_ALIAS
        self.SLAVE_DB_ALIAS = next(filter(lambda alias: alias != self.MASTER_DB_ALIAS, settings.DATABASES.keys()))
        self.DB_ALIASES = [self.MASTER_DB_ALIAS, self.SLAVE_DB_ALIAS]

    def db_is_online(self, db_alias):
        if self.offline_db_cache.get(db_alias):
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
        db_aliases = random.sample(self.DB_ALIASES, k=len(self.DB_ALIASES))
        for db_for_read in db_aliases:
            if self.db_is_online(db_for_read):
                log.debug(f'Read DB choice: {db_for_read}')
                return db_for_read
        raise ValueError('All databases are offline')

    def db_for_write(self, *args, **kwargs):
        db_for_write = self.MASTER_DB_ALIAS
        return db_for_write

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db in self.DB_ALIASES and obj2._state.db in self.DB_ALIASES:
            return True
        return None
