import os
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import requests
import steam.client
from background import keep_alive


def run_client(username, password, games_played):
  logging.info(f"Авторизация {username}")
  client = steam.client.SteamClient()
  try:
    client.cli_login(username=username, password=password)
    client.change_status(persona_state=7)
    client.games_played(games_played)
    client.run_forever()
  except Exception as e:
    logging.error(f"Ошибка при авторизации {username}: {e}")


def ping():
  while True:
    logging.info("Пингуем сервер")
    try:
      r = requests.get("https://ССЫЛКА на этот сервер") ####
      r.raise_for_status()
    except requests.exceptions.RequestException as e:
      logging.error(f"Ошибка при пинге сервера: {e}")
    time.sleep(300)


def main():
  logging.basicConfig(level=logging.INFO)

  executor = ThreadPoolExecutor(max_workers=3)

  users = [
    {
      "username": os.getenv("username1"),
      "password": os.getenv("password1"),
      "games_played": [570] #### id игры
    },
  ]

  for user in users:
    executor.submit(run_client, user["username"], user["password"],
                    user["games_played"])

  executor.submit(ping)

  executor.shutdown(wait=True)


if __name__ == "__main__":
  keep_alive()
  main()
