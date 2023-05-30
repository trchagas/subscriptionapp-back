# Aplicativo de gerenciamento de inscrições mensais: Backend

## Requirements

- Python 3.9+
- Python3 pip ( sudo apt install -y python3-pip )
- MySQL Dev: ( apt-get install -y libmysqlclient-dev )

## 1. Setup

### 1.1 Creating Flask virtualenv

(only needed first time)

```sh
  $ python3 -m venv venv
```

### 1.2 Activating Flask virtualenv

```sh
  $ source venv/bin/activate
```

From now on, you shall see **(venv)** written on the left side of command prompt, indicating that you're inside of the virtualenv

### 1.3 Installing requirements inside Flask virtualenv

(only needed first time)

```sh
  $ pip install -r requirements.txt
```

### 1.4 Configure needed environment variables inside .env file

(only needed first time. Examples available in **.env.production-example** and **.env.development-example**)

```sh
  $ cp .env.X-example .env
```

## 2. Migrate database && seed

```sh
  $ flask db stamp head
```

(The command above sets the pointer to the first migration. Only needed first time)

```sh
  $ flask db migrate
  $ flask db upgrade
  $ flask seed run
```

## 3. Run

(needs to be executed inside Flask virtualenv. See 1.2)

```sh
  $ python3 app.py
```

On another terminal, set up scheduled jobs:

```
  $ flask crontab add
```
