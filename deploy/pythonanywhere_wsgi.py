# =============================================================================
# PythonAnywhere WSGI 設定ファイルのテンプレート
# -----------------------------------------------------------------------------
# このファイルは「そのまま動かす」ためのものではなく、PythonAnywhere の
# Web タブにある WSGI 設定ファイル
#   /var/www/<ユーザー名>_pythonanywhere_com_wsgi.py
# の中身を、以下の内容で「置き換える」ためのテンプレートです。
#
# <ユーザー名> は自分の PythonAnywhere ユーザー名に置き換えてください。
# =============================================================================

import os
import sys

# --- プロジェクトのパスを Python のパスに追加 ---------------------------------
# git clone したディレクトリ（manage.py がある場所）を指定する。
path = '/home/<ユーザー名>/myRecordApp'
if path not in sys.path:
    sys.path.insert(0, path)

# --- 環境変数（本番用の設定値）-----------------------------------------------
# SECRET_KEY は必ず自分で生成した値に置き換える。
#   生成例（PythonAnywhere の Bash コンソールで）:
#   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
os.environ['DJANGO_SECRET_KEY'] = '<ここに生成した秘密鍵を貼る>'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = '<ユーザー名>.pythonanywhere.com'

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# --- Django アプリケーションを起動 -------------------------------------------
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
