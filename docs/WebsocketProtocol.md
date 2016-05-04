## Description

The protocol used to communicate moves to the server using json.

### Protocol
  Sent Message:
  ```json
  {
    "x": "<int>",
    "y": "<int>",
    "cid": "<base64>",
    "avatar" : "<css url>"
  }
  ```
  Response:
  ```json
  {
    "x": "<int>",
    "y": "<int>",
    "avatar" : "<url>",
    "cid" : "<base64>"
  }
  ```
