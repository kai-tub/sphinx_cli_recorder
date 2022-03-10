# Limitations

- ❌ _No_ Windows support
  - The underlying library that _records_ the terminal session does not support Windows terminals
  - Only tested on Linux
    - _Should_ work on other UNIX systems and macOS
- 🐌 Currently, all commands are always re-run since there is no way of knowing that an underlying command has been updated or not
  - A future version will support caching the result (see roadmap)
- 💣 To minimize the wait-time, all commands are executed in parallel in the background. The parallel execution may lead to a very high CPU/memory usage.
  - A future version could limit the number of subprocesses (see roadmap)
- 🐌 The first page-load will require synchronously downloading the JS script for the video-player
  - This will negatively affect the draw-time of the first-page load time
- Although the generated recordings are _a lot smaller_ than videos, the file size of many animation-heavy recordings could become relatively large
  - One idea is to re-use recordings across the entire web page if available (see roadmap)
