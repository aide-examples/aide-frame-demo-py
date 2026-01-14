# API Reference

Hello provides a simple HTTP API for name lookups.

## Endpoints

### POST /etymology

Look up information about a name.

**Request:**
```json
{
    "name": "Anna"
}
```

**Response:**
```json
{
    "name": "Anna",
    "meaning": "Grace, favor",
    "origin": "Hebrew (Hannah)",
    "gender": "feminine",
    "source": "demo"
}
```

### GET /status

Check if the service is running.

**Response:**
```json
{
    "ready": true,
    "api_configured": false
}
```

## Error Responses

| Status | Description |
|--------|-------------|
| 400 | Invalid JSON or missing name parameter |
| 404 | Endpoint not found |
