DATABASES = {
  'default': {
    'ENGINE'    : 'django.db.backends.mysql',
    'NAME'      : 'dweb',
    'USER'      : 'dweb',
    'PASSWORD'  : '<your_dweb_password>',
    'HOST'      : 'localhost',
    'PORT'      : '3306',
    'OPTIONS'   : {
      'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    },
  },
}