---
name: inoreader
description: Manage RSS feeds and articles via Inoreader API with BWS-backed OAuth2.
homepage: https://www.inoreader.com/developers
metadata: {"clawdbot":{"emoji":"📶"}}
---

# Inoreader Skill
The Inoreader Skill provides an interface for interacting with your Inoreader subscription data directly from your terminal. It manages OAuth2 authentication automatically using Bitwarden Secrets Manager (BWS).

## Configuration
Requires the following secrets in BWS:
- `INOREADER_CLIENT_ID`
- `INOREADER_CLIENT_SECRET`
- `INOREADER_ACCESS_TOKEN`
- `INOREADER_REFRESH_TOKEN`
- `INOREADER_TOKEN_EXPIRES_AT` (Unix timestamp)

The skill uses `bws-direct` and `bws-direct-put` for communication with your BWS vault. Ensure these commands are available in your path.

## Setup
### 1. Manual OAuth Flow (Initial Setup)
To authorize the application for the first time:
1. Run `./generate_auth_url_v3.sh` to get your authorization URL.
2. Visit the URL in your browser and authorize the app.
3. Your browser will redirect to `http://localhost:8080/?code=...`.
4. Copy the `code` parameter from the address bar.
5. Provide the code and your client secret to exchange for tokens.

### 2. Usage
Use the `inoreader.sh` script to execute API requests:

```bash
# Get unread counts
bash inoreader.sh unread-count

# Execute any API endpoint (relative to /reader/api/0/)
bash inoreader.sh <endpoint> [parameters]
```

## API Methods

All endpoints are relative to `https://www.inoreader.com/reader/api/0/`.

### Subscription & Feed Management
- **`subscription/list`**: Fetches the current feeds for the logged-in user.
- **`subscription/quickadd`**: Follows a new feed.
  - Parameters: `quickadd` (URL/Feed ID).
- **`subscription/edit`**: Rename a feed, add/remove from folder, or unfollow.
  - Parameters: `ac` (edit/follow/unfollow), `s` (feed ID), `t` (title), `a` (add label), `r` (remove label).

### Article & Stream Content
- **`stream/contents/[streamId]`**: Returns articles for a given collection (URL encoded streamId).
  - Parameters: `n` (items, max 100), `r` (order: `o` for oldest), `xt` (exclude tag), `it` (include tag), `c` (continuation token).
- **`stream/items/ids`**: Returns only article IDs for a stream (lighter weight).
  - Parameters: `s` (stream ID), `n` (max 1000).
- **`unread-count`**: Fetches unread counters for folders, tags, and feeds.

### Tags & Folders
- **`tag/list`**: Fetches current folders and tags for the user.
- **`rename-tag`**: Renames a tag or folder.
  - Parameters: `s` (source tag), `dest` (new name).
- **`disable-tag`**: Deletes a tag or folder.
  - Parameters: `s` (stream ID).
- **`edit-tag`**: Assigns tags to articles (read status, stars, labels).
  - Parameters: `a` (tag to add), `r` (tag to remove), `i` (item ID).
  - System tags: `user/-/state/com.google/read`, `user/-/state/com.google/starred`.
- **`mark-all-as-read`**: Marks all items in a stream as read.
  - Parameters: `s` (stream ID), `ts` (timestamp).

### User & Preferences
- **`user-info`**: Returns basic information about the logged-in user.
- **`preference/stream/list`**: List of folders and sort order preferences.
- **`preference/stream/set`**: Saves custom feed ordering.
  - Parameters: `s` (stream ID), `k` (key: `subscription-ordering`), `v` (value).

## Security & Maintenance
- **Automatic Token Rotation**: Before every request, the script checks if the token is within a 5-minute buffer of expiring. If so, it uses the `refresh_token` to fetch new credentials, which are pushed to BWS.
- **Secrets Management**: All sensitive data is kept in BWS and accessed only at runtime.
