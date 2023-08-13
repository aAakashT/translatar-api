# translatar-api
 Translation API Documentation

The Translation API allows you to translate text from one language to another using different translation services.

## Endpoint

- `/translate/`

## Authentication

- This API requires authentication using JWT tokens. Users must be authenticated to access this endpoint.


## API Overview

- **Endpoint:** `/api/translate/`
- **HTTP Method:** GET
- **Authentication:** JWT Token (Bearer token)
- **Permissions:** Authenticated users only


## Request

- Method: `GET`
- Headers:
  - `Authorization`: Bearer Token (JWT Token)

### Query Parameters

- `source`: Source language code (e.g., `en` for English)
- `target`: Target language code(s) separated by pluse sign (e.g., `hi+mr` for Hindi and Marathi or simply `hi` for hindi only)

### Request Parameters

- `text`: Text to be translated should be passed in list of dictionary
  (e.g. [{"text": "Hello"}])

## Response

- Status Code: `200 OK`
- Content:
  - `source_text`: Original source text
  - `translated_text`: Translated text
  - `source_language`: Source language code
  - `target_language`: Target language code(s)
  - `from_cache`: Whether the translation was retrieved from the cache

## Example Request:


```http```
GET /api/translate/?source=en&target=fr+mr
Authorization: Bearer <JWT_TOKEN>
request.body(json type):  [{"text": "Hello"}]



### Example Response:

```json```
{
    "source_text": [
        {
            "text": "Hello"
        }
    ],
    "translated_text": [
        {
            "translations": [
                {
                    "text": "नमस्कार",
                    "to": "hi"
                },
                {
                    "text": "नमस्कार",
                    "to": "mr"
                }
            ]
        }
    ],
    "source_language": "En",
    "target_language": [
        "hi",
        "mr"
    ],
    "from cache": "false"
}

### errors
HTTP 400 Bad Request: Missing or invalid parameters.
HTTP 401 Unauthorized: Invalid or missing JWT token.
HTTP 500 Internal Server Error: Translation service error.

### Caching
Translations are cached to optimize performance. If a translation is found in the cache, it is retrieved and marked as "from_cache" in the response.

## Usage Notes
To use this API, provide the required parameters in the query string.
Make sure to include a valid JWT token in the Authorization header.
