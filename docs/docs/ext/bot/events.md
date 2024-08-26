---
icon: material/clock-time-eleven-outline
hide:  
  - toc
---

# Event Handlers

## Bot Events
___


- `on_user_register`
    - **Description**: Triggered after a user successfully registers as a broadcaster.
    - **Data Type**:  [`Broadcaster`][twitch.user.Broadcaster]
    - **Usage**:
    ```python
    @client.event
    async def on_user_register(broadcaster: Broadcaster) -> None:
        ...
    ```