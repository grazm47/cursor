import argparse
import json
import os
import sys
import time
import uuid
import warnings
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLOR = True
except Exception:
    HAS_COLOR = False

GIGACHAT_OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
GIGACHAT_COMPLETIONS_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


class GigaChatAuthError(RuntimeError):
    pass


class GigaChatClient:
    def __init__(
        self,
        api_key_basic: str,
        scope: str = "GIGACHAT_API_PERS",
        verify_ssl_certs: bool = True,
        request_timeout_sec: int = 60,
    ) -> None:
        self.api_key_basic = api_key_basic
        self.scope = scope
        self.verify_ssl_certs = verify_ssl_certs
        self.request_timeout_sec = request_timeout_sec

        self._access_token: Optional[str] = None
        self._token_expire_epoch: float = 0.0

    def _fetch_access_token(self) -> None:
        headers = {
            "Authorization": f"Basic {self.api_key_basic}",
            "RqUID": str(uuid.uuid4()),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"scope": self.scope}

        try:
            response = requests.post(
                GIGACHAT_OAUTH_URL,
                headers=headers,
                data=data,
                timeout=self.request_timeout_sec,
                verify=self.verify_ssl_certs,
            )
        except RequestException as exc:
            raise GigaChatAuthError(f"Failed to connect to OAuth endpoint: {exc}")

        if response.status_code != 200:
            raise GigaChatAuthError(
                f"OAuth error {response.status_code}: {response.text}"
            )

        payload = response.json()
        access_token = payload.get("access_token")
        if not access_token:
            raise GigaChatAuthError("OAuth response missing access_token")

        # Fallback: if expires_in is provided, compute local epoch; otherwise refresh proactively after 25 minutes
        expires_in = payload.get("expires_in")
        if isinstance(expires_in, (int, float)):
            expire_epoch = time.time() + float(expires_in)
        else:
            expire_epoch = time.time() + 25 * 60

        # Add small safety margin
        self._access_token = access_token
        self._token_expire_epoch = expire_epoch - 30

    def _ensure_token(self) -> None:
        if not self._access_token or time.time() >= self._token_expire_epoch:
            self._fetch_access_token()

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "GigaChat",
        temperature: float = 0.4,
        top_p: float = 0.9,
        max_tokens: Optional[int] = None,
    ) -> str:
        self._ensure_token()

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Request-ID": str(uuid.uuid4()),
        }

        body: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
        }
        if max_tokens is not None:
            body["max_tokens"] = max_tokens

        try:
            response = requests.post(
                GIGACHAT_COMPLETIONS_URL,
                headers=headers,
                json=body,
                timeout=self.request_timeout_sec,
                verify=self.verify_ssl_certs,
            )
        except RequestException as exc:
            raise RuntimeError(f"Failed to connect to chat endpoint: {exc}")

        # If token expired mid-flight, refresh once and retry
        if response.status_code == 401:
            self._fetch_access_token()
            headers["Authorization"] = f"Bearer {self._access_token}"
            response = requests.post(
                GIGACHAT_COMPLETIONS_URL,
                headers=headers,
                json=body,
                timeout=self.request_timeout_sec,
                verify=self.verify_ssl_certs,
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"Chat error {response.status_code}: {response.text}"
            )

        payload = response.json()
        # OpenAI-compatible-ish: { choices: [ { message: { content } } ] }
        try:
            content = payload["choices"][0]["message"]["content"]
        except Exception:
            # Fallback: print full payload for diagnostics
            raise RuntimeError(f"Unexpected response format: {json.dumps(payload, ensure_ascii=False)}")

        return content


def _color(text: str, color: Optional[str], no_color: bool) -> str:
    if no_color or not HAS_COLOR or not color:
        return text
    return f"{color}{text}{Style.RESET_ALL}"


def build_system_prompt() -> str:
    return (
        "Ты — вежливый и проактивный ассистент‑продавец. Отвечай кратко и по делу на русском языке. "
        "Уточняй потребности, предлагай подходящие товары, объясняй выгоды простыми словами, "
        "предлагай следующий шаг (добавить в корзину, оформить заказ, показать ещё варианты). "
        "Если чего-то не знаешь — скажи честно и предложи альтернативу. Не придумывай фактов. "
        "Для восприятия используй маркированные списки, когда это уместно."
    )


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Терминальный ассистент‑продавец на базе GigaChat",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--api-key",
        dest="api_key",
        default=None,
        help="API ключ GigaChat (строка для заголовка Authorization: Basic ...). Можно также задать через переменную окружения GIGACHAT_API_KEY.",
    )
    parser.add_argument(
        "--scope",
        default=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
        help="OAuth scope для запроса токена (обычно GIGACHAT_API_PERS или GIGACHAT_API_CORP)",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("GIGACHAT_MODEL", "GigaChat"),
        help="Модель GigaChat",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=float(os.getenv("GIGACHAT_TEMPERATURE", 0.4)),
        help="Креативность ответа",
    )
    parser.add_argument(
        "--top-p",
        type=float,
        default=float(os.getenv("GIGACHAT_TOP_P", 0.9)),
        help="Ядерная выборка (top_p)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=(
            int(os.getenv("GIGACHAT_MAX_TOKENS"))
            if os.getenv("GIGACHAT_MAX_TOKENS")
            else None
        ),
        help="Ограничение на длину ответа (токены)",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Отключить проверку TLS-сертификата (если возникают проблемы с цепочкой доверия)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Отключить цветной вывод",
    )
    parser.add_argument(
        "--system",
        default=os.getenv("SALES_ASSISTANT_SYSTEM_PROMPT", build_system_prompt()),
        help="Системное сообщение (роль ассистента)",
    )

    args = parser.parse_args(argv)

    # Fill API key from env if not provided explicitly
    if not args.api_key:
        args.api_key = os.getenv("GIGACHAT_API_KEY")

    return args


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    if not args.api_key:
        print(
            "[Ошибка] Не задан API ключ. Передайте --api-key или установите переменную GIGACHAT_API_KEY",
            file=sys.stderr,
        )
        return 2

    if args.insecure:
        warnings.simplefilter("ignore", InsecureRequestWarning)

    client = GigaChatClient(
        api_key_basic=args.api_key,
        scope=args.scope,
        verify_ssl_certs=(not args.insecure),
    )

    hello = _color("Ассистент‑продавец GigaChat", Fore.GREEN if HAS_COLOR else None, args.no_color)
    print(hello)
    print("Команды: /reset — сбросить контекст, /exit — выйти, /help — помощь")

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": args.system},
    ]

    while True:
        try:
            user_text = input(
                _color("Покупатель: ", Fore.CYAN if HAS_COLOR else None, args.no_color)
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            return 0

        if not user_text:
            continue

        if user_text in {"/exit", "/quit", "/q"}:
            print("До свидания!")
            return 0
        if user_text in {"/help", "/h"}:
            print("Доступные команды: /reset — очистить диалог, /exit — выйти")
            continue
        if user_text in {"/reset", "/r"}:
            messages = [{"role": "system", "content": args.system}]
            print("Контекст очищен.")
            continue

        messages.append({"role": "user", "content": user_text})

        try:
            reply = client.chat_completion(
                messages=messages,
                model=args.model,
                temperature=args.temperature,
                top_p=args.top_p,
                max_tokens=args.max_tokens,
            )
        except Exception as exc:
            err = _color(f"Ошибка: {exc}", Fore.RED if HAS_COLOR else None, args.no_color)
            print(err, file=sys.stderr)
            # Do not append assistant message on error
            continue

        messages.append({"role": "assistant", "content": reply})
        print(_color("Ассистент:", Fore.YELLOW if HAS_COLOR else None, args.no_color))
        print(reply)


if __name__ == "__main__":
    sys.exit(main())