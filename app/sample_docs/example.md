# Example Document

This is a sample document in the `samples/` custom root.

## Features

- Standard Markdown formatting
- Works like docs and help viewers
- App-defined title and route

## Code Example

```python
# Configure a custom root
config = http_routes.DocsConfig(
    app_name="My App",
    custom_roots={
        "samples": http_routes.CustomRoot(
            dir_key="SAMPLES_DIR",
            title="Samples",
            route="/samples",
            subdir="samples",
        )
    }
)
```
