---
icon: material/clock-time-eleven-outline
hide:  
  - toc
---

# Event Handlers

## Overlay Events
___

- `on_overlay_ready`
    - **Description**: Triggered when the overlay is ready for interaction.
    - **Usage**:
    ```python
    @client.event
    async def on_overlay_ready() -> None:
        ...
    ```

- `on_overlay_alert(default: str, data: Dict[str, Any])`
    - **Description**: Triggered when an alert is sent.
    - **Data Type**: 
      - `default`: `str` - The filter parameter for the alert (e.g., 'special').
      - `data`: `Dict[str, Any]` - The details of the alert.
    - **Usage**:
    ```python
    @client.event
    async def on_overlay_alert(default: str, data: Dict[str, Any]) -> None:
        ...
    ```