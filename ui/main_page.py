# from __future__ import annotations

# import random

# import flet as ft


# EMBEDDING_DIMENSION = 5


# def make_random_embedding() -> list[float]:
#     return [round(random.uniform(-1, 1), 3) for _ in range(EMBEDDING_DIMENSION)]


# def build_main_page(page: ft.Page) -> None:
#     page.title = "Tokenization Demo"
#     page.window_width = 780
#     page.window_height = 620
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.padding = 24
#     page.bgcolor = ft.Colors.BLUE_GREY_50

#     status_text = ft.Text(size=14, color=ft.Colors.RED_700)
#     word_text = ft.Text("Input word: -", size=18, weight=ft.FontWeight.W_600)
#     tokens_array_text = ft.Text("Tokens array: []", selectable=True)
#     token_ids_text = ft.Text("Token IDs: []", selectable=True)
#     embeddings_text = ft.Text("Embeddings: []", selectable=True)
#     token_boxes = ft.Row(spacing=14, wrap=True)

#     word_input = ft.TextField(
#         label="Enter a word",
#         hint_text="Enter 3-letter word",
#         width=280,
#         max_length=3,
#         autofocus=True,
#         border_radius=8,
#         text_size=18,
#         capitalization=ft.TextCapitalization.NONE,
#     )

#     def set_status(message: str, is_error: bool = True) -> None:
#         status_text.value = message
#         status_text.color = ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700

#     def input_changed(_: ft.ControlEvent) -> None:
#         cleaned = "".join(char for char in (word_input.value or "").lower() if char.isalpha())
#         cleaned = cleaned[:3]
#         if word_input.value != cleaned:
#             word_input.value = cleaned
#             set_status("Letters mattum type pannunga. Maximum 3 letters.", is_error=True)
#         else:
#             status_text.value = ""
#         page.update()

#     word_input.on_change = input_changed

#     def validate_word() -> tuple[bool, str, str]:
#         word = (word_input.value or "").strip().lower()

#         if word == "":
#             return False, word, "Word type pannunga."
#         if len(word) < 3:
#             return False, word, "Correct-a 3 letters venum."
#         if len(word) > 3:
#             return False, word, "3 letters-ku mela poda koodathu."
#         if not word.isalpha():
#             return False, word, "Number, space, symbol poda koodathu."

#         return True, word, ""

#     def make_token_box(token: str, token_id: int, embedding: list[float]) -> ft.Container:
#         return ft.Container(
#             width=210,
#             bgcolor=ft.Colors.WHITE,
#             border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
#             border_radius=8,
#             padding=14,
#             content=ft.Column(
#                 controls=[
#                     ft.Container(
#                         width=70,
#                         height=58,
#                         alignment=ft.Alignment.CENTER,
#                         bgcolor=ft.Colors.BLUE_50,
#                         border=ft.Border.all(1, ft.Colors.BLUE_200),
#                         border_radius=8,
#                         content=ft.Text(token, size=30, weight=ft.FontWeight.BOLD),
#                     ),
#                     ft.Text(f"Token ID: {token_id}", weight=ft.FontWeight.W_600),
#                     ft.Text(f"Embedding: {embedding}", selectable=True),
#                 ],
#                 spacing=8,
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             ),
#         )

#     def tokenize_click(_: ft.ControlEvent) -> None:
#         valid, word, message = validate_word()
#         if not valid:
#             set_status(message)
#             page.update()
#             return

#         tokens = list(word)
#         token_ids = list(range(len(tokens)))
#         embeddings = [make_random_embedding() for _ in tokens]

#         word_text.value = f"Input word: {word}"
#         tokens_array_text.value = f"Tokens array: {tokens}"
#         token_ids_text.value = f"Token IDs: {token_ids}"
#         embeddings_text.value = f"Embeddings: {embeddings}"
#         token_boxes.controls = [
#             make_token_box(token, token_id, embedding)
#             for token, token_id, embedding in zip(tokens, token_ids, embeddings)
#         ]
#         set_status("Tokenization complete.", is_error=False)
#         page.update()

#     def clear_click(_: ft.ControlEvent) -> None:
#         word_input.value = ""
#         status_text.value = ""
#         word_text.value = "Input word: -"
#         tokens_array_text.value = "Tokens array: []"
#         token_ids_text.value = "Token IDs: []"
#         embeddings_text.value = "Embeddings: []"
#         token_boxes.controls.clear()
#         page.update()

#     page.add(
#         ft.Column(
#             controls=[
#                 ft.Text("Miniature of very small LLM", size=28, weight=ft.FontWeight.BOLD),
#                 ft.Text(
#                     "Single input box-la 3 letters type pannunga. App split panni tokens kaamikum.",
#                     color=ft.Colors.BLUE_GREY_700,
#                 ),
#                 ft.Row(
#                     controls=[
#                         word_input,
#                         ft.ElevatedButton(
#                             "Tokenize",
#                             icon=ft.Icons.PLAY_ARROW,
#                             on_click=tokenize_click,
#                             height=48,
#                             margin=ft.Margin(top=0, right=0, bottom=20, left=0),
#                         ),
#                         ft.OutlinedButton(
#                             "Clear",
#                             icon=ft.Icons.CLEAR,
#                             on_click=clear_click,
#                             height=48,
#                             margin=ft.Margin(top=0, right=0, bottom=20, left=0),
#                         ),
#                     ],
#                     vertical_alignment=ft.CrossAxisAlignment.END,
#                     spacing=10,
#                 ),
#                 status_text,
#                 ft.Container(
#                     bgcolor=ft.Colors.WHITE,
#                     border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
#                     border_radius=8,
#                     padding=16,
#                     content=ft.Column(
#                         controls=[
#                             word_text,
#                             tokens_array_text,
#                             token_ids_text,
#                             embeddings_text,
#                         ],
#                         spacing=8,
#                     ),
#                 ),
#                 ft.Text("Split Tokens", size=18, weight=ft.FontWeight.W_600),
#                 token_boxes,
#             ],
#             spacing=16,
#             scroll=ft.ScrollMode.AUTO,
#         )
#     )


from __future__ import annotations

import flet as ft

from auth.auth_service import (
    AuthenticationError,
    create_access_token,
    hash_password,
    verify_access_token,
    verify_password,
)
from config.settings import get_database_settings, get_model_settings
from database.db import Database, DatabaseError
from embedding.embedding_service import EmbeddingService, EmbeddingServiceError
from tokenizer.tokenizer_service import TokenizerService, TokenizerServiceError


# def build_main_page(page: ft.Page) -> None:
#     page.title = "Tokenization Demo"
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.bgcolor = ft.Colors.BLUE_GREY_50
#     page.padding = 12
#     page.scroll = ft.ScrollMode.AUTO

def build_main_page(page: ft.Page) -> None:
    page.title = "Tokenization Demo"
    page.expand = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.padding = 12
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO

    database = Database(get_database_settings())
    model_settings = get_model_settings()
    tokenizer_service = TokenizerService(model_settings.tokenizer_model)
    embedding_service = EmbeddingService(model_settings.embedding_model)
    session = {"token": ""}

    try:
        database.initialize()
        database_status = ""
    except DatabaseError as exc:
        database_status = str(exc)

    status_text = ft.Text(size=14)
    word_text = ft.Text("Input word: -", size=18, weight=ft.FontWeight.W_600)
    transformer_tokens_text = ft.Text("Transformer tokens: -", selectable=True)
    token_boxes = ft.Row(
        spacing=12,
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    word_input = ft.TextField(
        label="Enter a word",
        hint_text="Enter 3-letter word",
        expand=True,
        max_length=3,
        autofocus=True,
        border_radius=8,
        text_size=18,
        capitalization=ft.TextCapitalization.NONE,
        # token_boxes = ft.Row(spacing=14, wrap=True)
    )

    def set_status(message: str, is_error: bool = True) -> None:
        status_text.value = message
        status_text.color = (
            ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700
        )

    def input_changed(_: ft.ControlEvent) -> None:
        cleaned = "".join(
            char for char in (word_input.value or "").lower()
            if char.isalpha()
        )[:3]

        if word_input.value != cleaned:
            word_input.value = cleaned
            set_status("Letters mattum type pannunga. Maximum 3 letters.")
        else:
            status_text.value = ""

        page.update()

    word_input.on_change = input_changed

    def validate_word() -> tuple[bool, str, str]:
        word = (word_input.value or "").strip().lower()

        if not word:
            return False, word, "Word type pannunga."
        if len(word) != 3:
            return False, word, "Correct-a 3 letters venum."
        if not word.isalpha():
            return False, word, "Number, space, symbol poda koodathu."

        return True, word, ""

    def make_token_box(
        token: str,
        token_id: int,
        embedding: list[float],
    ) -> ft.Container:
        return ft.Container(
            width=220,
            height=300,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
            border_radius=8,
            padding=12,
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=60,
                        height=55,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=ft.Colors.BLUE_50,
                        border=ft.Border.all(1, ft.Colors.BLUE_200),
                        border_radius=8,
                        content=ft.Text(
                            token,
                            size=28,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ),
                    ft.Text(
                        f"Token ID: {token_id}",
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Text(
                        f"Embedding: {embedding[:6]}...",
                        selectable=True,
                        size=12,
                        max_lines=8,
                    ),
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def tokenize_click(_: ft.ControlEvent) -> None:
        valid, word, message = validate_word()

        if not valid:
            set_status(message)
            page.update()
            return

        try:
            verify_access_token(session["token"])
        except AuthenticationError as exc:
            set_status(str(exc))
            page.update()
            return

        try:
            token_items = tokenizer_service.tokenize_characters(word)
            embeddings = embedding_service.embed_tokens(token_items)
            database.save_history(word, embeddings)
        except (TokenizerServiceError, EmbeddingServiceError, DatabaseError) as exc:
            set_status(str(exc))
            page.update()
            return

        word_text.value = f"Input word: {word}"
        transformer_tokens_text.value = (
            "Transformer tokens: "
            + " | ".join(f"{item.token} ({item.token_id})" for item in token_items)
        )

        token_boxes.controls = [
            make_token_box(item.token, item.token_id, item.vector)
            for item in embeddings
        ]

        set_status("Tokenization complete.", is_error=False)
        page.update()

    def clear_click(_: ft.ControlEvent) -> None:
        word_input.value = ""
        status_text.value = ""
        word_text.value = "Input word: -"
        transformer_tokens_text.value = "Transformer tokens: -"
        token_boxes.controls.clear()
        page.update()

    auth_title = ft.Text("Login", size=26, weight=ft.FontWeight.BOLD)
    email_input = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
    password_input = ft.TextField(label="Password", password=True, can_reveal_password=True)
    auth_status = ft.Text(size=14)
    auth_mode = {"register": False}

    def set_auth_status(message: str, is_error: bool = True) -> None:
        auth_status.value = message
        auth_status.color = ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700

    def switch_auth_mode(_: ft.ControlEvent) -> None:
        auth_mode["register"] = not auth_mode["register"]
        auth_title.value = "Register" if auth_mode["register"] else "Login"
        auth_action.content = "Register" if auth_mode["register"] else "Login"
        auth_switch.content = (
            "Already have an account? Login"
            if auth_mode["register"]
            else "Need an account? Register"
        )
        set_auth_status("", is_error=False)
        page.update()

    def auth_action_click(_: ft.ControlEvent) -> None:
        email = (email_input.value or "").strip().lower()
        password = password_input.value or ""

        if "@" not in email or not password:
            set_auth_status("Enter a valid email and password.")
            page.update()
            return

        try:
            if auth_mode["register"]:
                database.create_user(email, hash_password(password))
                auth_mode["register"] = False
                auth_title.value = "Login"
                auth_action.content = "Login"
                auth_switch.content = "Need an account? Register"
                password_input.value = ""
                set_auth_status("Account created. Please login.", is_error=False)
                page.update()
                return

            user = database.get_user(email)
            if not user or not verify_password(password, user["password_hash"]):
                set_auth_status("Invalid email or password.")
                page.update()
                return
            user_id = int(user["id"])

            session["token"] = create_access_token(user_id, email)
            auth_screen.visible = False
            app_content.visible = True
            set_status(f"Logged in as {email}.", is_error=False)
            page.update()
        except (DatabaseError, AuthenticationError) as exc:
            set_auth_status(str(exc))
            page.update()

    auth_action = ft.ElevatedButton("Login", on_click=auth_action_click, height=46)
    auth_switch = ft.TextButton("Need an account? Register", on_click=switch_auth_mode)
    auth_panel = ft.Container(
        width=420,
        padding=32,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        content=ft.Column(
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[auth_title, email_input, password_input, auth_action, auth_switch, auth_status],
        ),
    )
    auth_screen = ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_50,
        content=auth_panel,
    )
    if database_status:
        set_auth_status(database_status)

    # page.add(
    #     ft.Column(
    #         expand=True,
    #         spacing=14,
    #         controls=[
    #             ft.Text(
    #                 "Miniature of very small LLM",
    #                 size=26,
    #                 weight=ft.FontWeight.BOLD,
    #             ),
    #             ft.Text(
    #                 "Single input box-la 3 letters type pannunga. "
    #                 "App split panni tokens kaamikum.",
    #                 color=ft.Colors.BLUE_GREY_700,
    #             ),
    #             ft.Column(
    #                 spacing=8,
    #                 controls=[
    #                     word_input,
    #                     ft.Row(
    #                         wrap=True,
    #                         spacing=8,
    #                         controls=[
    #                             ft.ElevatedButton(
    #                                 "Tokenize",
    #                                 icon=ft.Icons.PLAY_ARROW,
    #                                 on_click=tokenize_click,
    #                                 height=46,
    #                             ),
    #                             ft.OutlinedButton(
    #                                 "Clear",
    #                                 icon=ft.Icons.CLEAR,
    #                                 on_click=clear_click,
    #                                 height=46,
    #                             ),
    #                         ],
    #                     ),
    #                 ],
    #             ),
    #             status_text,
    #             ft.Container(
    #                 width=float("inf"),
    #                 bgcolor=ft.Colors.WHITE,
    #                 border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
    #                 border_radius=8,
    #                 padding=14,
    #                 content=ft.Column(
    #                     controls=[
    #                         word_text,
    #                         tokens_array_text,
    #                         token_ids_text,
    #                         embeddings_text,
    #                     ],
    #                     spacing=8,
    #                 ),
    #             ),
    #             ft.Text(
    #                 "Split Tokens",
    #                 size=18,
    #                 weight=ft.FontWeight.W_600,
    #             ),
    #             token_boxes,
    #         ],
    #     )
    # )


    
    app_content = ft.Container(
        visible=False,
        expand=True,
        padding=16,
        bgcolor=ft.Colors.BLUE_GREY_50,
        content=ft.Column(
                expand=True,
                spacing=14,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text(
                        "Miniature of very small LLM",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Type 3 letters into a single input box. The app will split them and display the tokens.",
                        color=ft.Colors.BLUE_GREY_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        width=float("inf"),
                        content=word_input,
                    ),
                    ft.Row(
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.ElevatedButton(
                                "Tokenize",
                                icon=ft.Icons.PLAY_ARROW,
                                on_click=tokenize_click,
                                height=46,
                            ),
                            ft.OutlinedButton(
                                "Clear",
                                icon=ft.Icons.CLEAR,
                                on_click=clear_click,
                                height=46,
                            ),
                        ],
                    ),
                    status_text,
                    ft.Container(
                        width=float("inf"),
                        bgcolor=ft.Colors.WHITE,
                        border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                        border_radius=8,
                        padding=14,
                        content=ft.Column(
                            controls=[word_text, transformer_tokens_text],
                            spacing=8,
                        ),
                    ),
                    ft.Text(
                        "Split Tokens",
                        size=18,
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    token_boxes,
                ],
            ),
    )

    page.add(auth_screen, app_content)