---
title: Polyglot Programming
---
**Polyglot programming** is the practice of using multiple programming languages to build a single application, leveraging each language's strengths. This approach involves running different parts of an application written in different languages and coordinating them to work together as one system.
# 1. HTTP Requests (REST API)
**Best for:** Synchronous communication (Request/Response) and standard web apps.

This is the industry standard. You turn one component (e.g., Python) into a "Server" and the other (Ruby) into a "Client." The client sends data via a URL, and the server processes it and sends an answer back.
- **The Python Side:** You use a lightweight framework like **Flask** or **FastAPI** to listen on a local port (e.g., `localhost:5000`).
- **The Ruby Side:** You use an HTTP client library like **Faraday** or **HTTParty** to send JSON data to that port.

> **Example flow:** Ruby sends a `POST` request with `{ "user_id": 5 }` to Python. Python calculates a score and returns `{ "score": 95 }`. Ruby receives the score immediately.

# 2. Message Broker (Redis)
**Best for:** Asynchronous background jobs, high speed, or "Fire and Forget."

If the two components don't need to talk instantly (e.g., Python queues a job, Ruby processes it later) or if you need high-speed real-time messaging, **Redis** is the best local tool. It acts as a middleman.
- **Shared Space:** Both Python and Ruby connect to the same local Redis instance.
- **Pub/Sub Pattern:** Python "Publishes" a message to a channel (e.g., `updates`). Ruby "Subscribes" to that channel and reacts whenever a message arrives.
- **Queue Pattern:** Python pushes an item into a list; Ruby pops it off and processes it.

# 3. Subprocesses (Shell Execution)
**Best for:** Simple scripts where one controls the other tightly.

If one script is the "Master" and just needs to run the other script to get a result, you don't need networking. You can simply execute the other language's command line interface.
- **How it works:** The Python script uses the `subprocess` library to run `ruby script.rb`.
- **Data Transfer:** Python sends data via **Standard Input (stdin)** and reads the result from Ruby's **Standard Output (stdout)**.

> **Note:** This is simple to set up but hard to scale. If the Ruby script crashes or hangs, it can freeze the Python script.

# 4. Shared Files (File I/O)
**Best for:** Large data processing or legacy systems.

Both scripts agree on a specific file path (e.g., `data.json`). One writes to it, and the other reads from it.
- **Constraint:** You usually need a mechanism to tell the second script _when_ the file is ready (like creating a secondary "lock" file or using a file-watcher library).
- **Downside:** This is generally the slowest method and prone to "race conditions" (where one reads while the other is still writing).

| **Method**       | **Complexity**         | **Speed** | **Best Use Case**                      |
| ---------------- | ---------------------- | --------- | -------------------------------------- |
| **HTTP (REST)**  | Medium                 | Medium    | Standard services, easy to debug.      |
| **Redis**        | Low (requires install) | Very High | Real-time data or background queues.   |
| **Subprocess**   | Low                    | High      | One script simply "running" the other. |
| **Shared Files** | Low                    | Low       | Large batch processing.                |

**Simple Example with Python (FastAPI) and Ruby (Faraday)**
Run them in separate terminals.

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 1. Define the data shape we expect from Ruby
class Numbers(BaseModel):
    x: int
    y: int

@app.get("/")
def read_root():
    return {"status": "Python server is running"}

# 2. Create the endpoint that receives data
@app.post("/add")
def add_numbers(data: Numbers):
    result = data.x + data.y
    print(f"Received {data.x} and {data.y} from Ruby. Result: {result}")
    return {"operation": "addition", "result": result}

if __name__ == "__main__":
    # Run the server on localhost port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

```ruby
require 'faraday'
require 'json'

# 1. Configure the connection to the Python app
url = 'http://127.0.0.1:8000'
conn = Faraday.new(url: url)

puts "--- Ruby Client Starting ---"

# 2. Prepare the payload
payload = { x: 50, y: 100 }

# 3. Send the POST request
response = conn.post('/add') do |req|
  req.headers['Content-Type'] = 'application/json'
  req.body = payload.to_json
end

# 4. Handle the response
if response.status == 200
  data = JSON.parse(response.body)
  puts "Success! Python answered:"
  puts "Result: #{data['result']}"
else
  puts "Error: #{response.status}"
end
```

> They can also be containerized with Docker so they can communicate without needing manual terminal setups.

