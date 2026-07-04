# PythonAnywhere デプロイ手順（myRecordApp）

Django 製の日本酒記録アプリを PythonAnywhere（無料アカウントで可）にデプロイする手順です。
`<ユーザー名>` は自分の PythonAnywhere ユーザー名に読み替えてください。

---

## 0. 事前準備（ローカル）

このプロジェクトはすでに Git 初期化・本番対応済みです。あとは GitHub 等の
リモートリポジトリに push するだけです。

```bash
# GitHub で空のリポジトリを作成した後、ローカルで:
git remote add origin https://github.com/<あなたのGitHub名>/myRecordApp.git
git branch -M main
git push -u origin main
```

> ⚠️ **Python バージョンについて**
> ローカルは Python 3.14 ですが、PythonAnywhere が対応する最新版は 3.13 の
> ことが多いです。Django 6.0 は Python 3.12 / 3.13 で動作するので、
> PythonAnywhere 側では **Python 3.13** の仮想環境を作れば問題ありません。
> （下記手順は 3.13 を前提にしています。利用可能な最新版に読み替えてください）

---

## 1. コードを取得（PythonAnywhere の Bash コンソール）

PythonAnywhere にログイン →「Consoles」→「Bash」を開いて実行:

```bash
git clone https://github.com/<あなたのGitHub名>/myRecordApp.git
cd myRecordApp
```

---

## 2. 仮想環境を作成して依存パッケージをインストール

```bash
python3.13 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. 本番用の環境変数を設定してマイグレーション

秘密鍵を生成しておきます（この値は手順 6 の WSGI ファイルに貼ります）:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

DB のマイグレーションと静的ファイルの集約を実行:

```bash
export DJANGO_SECRET_KEY='<生成した秘密鍵>'
export DJANGO_DEBUG='False'
export DJANGO_ALLOWED_HOSTS='<ユーザー名>.pythonanywhere.com'

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser   # 管理画面用（任意）
```

---

## 4. Web アプリを作成（Web タブ）

1. 「Web」タブ →「Add a new web app」
2. ドメインはそのまま（`<ユーザー名>.pythonanywhere.com`）で次へ
3. フレームワーク選択で **「Manual configuration」** を選ぶ（Django の自動設定は使わない）
4. Python バージョンは **3.13** を選ぶ

---

## 5. 仮想環境のパスを設定（Web タブ）

「Web」タブの **Virtualenv** セクションに以下を入力:

```
/home/<ユーザー名>/myRecordApp/venv
```

---

## 6. WSGI 設定ファイルを編集（Web タブ）

「Web」タブの **Code** セクションにある WSGI 設定ファイル
（`/var/www/<ユーザー名>_pythonanywhere_com_wsgi.py`）のリンクをクリックし、
中身を **すべて削除** して、本リポジトリの
[`deploy/pythonanywhere_wsgi.py`](./pythonanywhere_wsgi.py) の内容に置き換えます。

その際、ファイル内の以下を自分の値に書き換えてください:

- `<ユーザー名>` → PythonAnywhere のユーザー名
- `DJANGO_SECRET_KEY` → 手順 3 で生成した秘密鍵
- `DJANGO_ALLOWED_HOSTS` → `<ユーザー名>.pythonanywhere.com`

保存したら Web タブに戻ります。

---

## 7. 静的ファイル / メディアのマッピング（Web タブ）

「Web」タブの **Static files** セクションで 2 つ登録します:

| URL        | Directory                                        |
|------------|--------------------------------------------------|
| `/static/` | `/home/<ユーザー名>/myRecordApp/staticfiles`      |
| `/media/`  | `/home/<ユーザー名>/myRecordApp/media`            |

（管理画面や今後の CSS、アップロード画像を正しく配信するために必要です）

---

## 8. リロードして公開

「Web」タブ上部の緑の **「Reload」** ボタンを押します。

ブラウザで以下にアクセスして確認:

- アプリ: `https://<ユーザー名>.pythonanywhere.com/`
- 管理画面: `https://<ユーザー名>.pythonanywhere.com/admin/`

---

## 更新をデプロイするとき

ローカルで変更を push した後、PythonAnywhere の Bash コンソールで:

```bash
cd ~/myRecordApp
git pull
source venv/bin/activate
pip install -r requirements.txt          # 依存が増えたときのみ
python manage.py migrate                 # モデル変更があったときのみ
python manage.py collectstatic --noinput # 静的ファイルを変えたときのみ
```

その後、「Web」タブで **「Reload」** を押せば反映されます。

---

## トラブルシュート

- **エラー画面が出る** → Web タブの「Error log」を確認。多くは WSGI ファイルの
  パス・ユーザー名・秘密鍵の記入漏れ。
- **CSS が当たらない / 管理画面が崩れる** → 手順 7 の `/static/` マッピングと、
  `collectstatic` の実行を確認。
- **DisallowedHost エラー** → WSGI ファイルの `DJANGO_ALLOWED_HOSTS` が
  実際のドメインと一致しているか確認。
- **フォーム送信で 403（CSRF）** → `DJANGO_ALLOWED_HOSTS` が正しく設定されていれば
  `settings.py` が自動で `CSRF_TRUSTED_ORIGINS` を組み立てます。ドメインの綴りを確認。

> 補足: このアプリは Tailwind を CDN（`https://cdn.tailwindcss.com`）で読み込んで
> いるため、CSS 自体のビルドは不要です。`collectstatic` が必要なのは主に
> Django 管理画面の静的ファイルのためです。
