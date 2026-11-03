# Requirements — Room Lighting (demo spec, covered)

The demo house needs lights in every room.

- The lights controller lives in app/lights.py and must expose a
  `lights_on()` function.
- The spec also mentions app/missing.py — that file does not exist
  in the demo house, on purpose, so Spec Ghost reports this spec
  as stale as well as covered. A spec can be both: covered (code
  references it) and stale (it points at a deleted file).
