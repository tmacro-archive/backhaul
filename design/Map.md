# Game State Storage

## Architecture

```
			+-------------------------+   +-------------------------+
			|       Game Client       |   |       Game Server       |
			|-------------------------|   |-------------------------|
			|                         |   |                         |
			| +---------------------+ |   | +---------------------+ |
			| |         UI          | |   | |   Game Simulation   | |
			| +---------------------+ |   | +---------------------+ |
			|           ^+            |   |           ^+            |
			|           ||            |   |           ||            |
			|           +v            |   |           +v            |
			| +---------------------+ |   | +---------------------+ |
			| |     Game State      | |   | |     Game State      | |
			| |---------------------| |   | |---------------------| |
			| |         ^+          | |   | |         ^+          | |
			| |         ||          | |   | |         ||          | |
			| |         +v          | |   | |         +v          | |
			| | +-----------------+ | |   | | +-----------------+ | |
			| | |   Change Log    | | |   | | |   Change Log    | | |
			| | |-----------------| | |   | | |-----------------| | |
			| | |       ^+        +----------->       ^+        | | |
			| | |       ||        <-----------+       ||        | | |
			| | |       +v        | | |   | | |       +v        | | |
			| | | +-------------+ | | |   | | | +-------------+ | | |
			| | | | Local unqlite | | | |   | | | | Local unqlite | | | |
			| | | |             | | | |   | | | |             | | | |
			+-+-+-+-------------+-+-+-+   +-+-+-+-------------+-+-+-+
```

## Component Breakdown

### Game State
 This represents the high level object presented the the consuming application.
 At this level methods and responses should consume and produce high level game objects, with no "knowledge" of the underlying db leaking through.
