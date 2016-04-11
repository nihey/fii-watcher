# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False

    CASPER_PATH = 'casperjs'

    LISTER_PATH = '../watcher/bin/list'
    WATCHER_PATH = '../watcher/bin/watch'

    FEED_WORKERS = 20

    RDBMS = 'postgresql'
    DB_NAME = 'fii_watch'
    DB_USER = 'nihey'
    DB_PASS = ''
    DB_PORT = 5432
    DB_HOST = 'localhost'

    MAILER_URL = ''

    FII_CHANGE_SUBJECT = "[FII] {fii_code} - {subject}"
    FII_CHANGE_BODY = """
Uma nova notícia foi postada em {fii_code}, para acessa-la clique em:

{link}

ou

{url}

- Nihey Takizawa
"""

    FII_GENERIC_CHANGE_SUBJECT = "[FII] Alteração na página de {fii_code}"
    FII_GENERIC_CHANGE_BODY = """
Alguma alteração ocorreu na página de {fii_code}, para acessa-la clique em:

{url}

Isto pode ter sido causado por uma falha nos sistemas da BM&FBovespa, ou uma
mudança no layout da página.

- Nihey Takizawa
"""
