DATABASES = {
  'default': {
    'ENGINE'    : 'django.db.backends.mysql',
    'NAME'      : 'dweb',
    'USER'      : 'dweb',
    'PASSWORD'  : 'Dweb@777',
    'HOST'      : 'localhost',
    'PORT'      : '3306',
    'OPTIONS'   : {
      'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    },
  },
}