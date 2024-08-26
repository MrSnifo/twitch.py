---
icon: material/clock-time-eleven-outline
hide:  
  - toc
---

# Event Handlers

## Oauth Events
___

- `on_code`
    - **Description**: Triggered when the device authentication flow generates a code for verification.
    - **Usage**:
    ```python
    @client.event
    async def on_code(code: str) -> None:
        print(f'Verification URI: https://www.twitch.tv/activate?device-code={code}')
    ```

---

- `on_auth`
    - **Description**: Triggered after successful authentication, providing the access and refresh tokens.
    - **Usage**:
    ```python
    @client.event
    async def on_auth(access_token: str, refresh_token: str) -> None:
        ...
    ```
