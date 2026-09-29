// All communication with the FastAPI backend lives in this one file.

const API_URL = "http://127.0.0.1:8000/chat";

export async function sendMessage(message) {
  let res;

  try {
    res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
  } catch {
    // fetch itself failed: backend is off or unreachable
    throw new Error(
      "Cannot reach the Resolv.ai backend. Please make sure the FastAPI server is running."
    );
  }

  if (!res.ok) {
    // Backend replied with an error (e.g. 503 when Ollama is off)
    let detail = "Something went wrong. Please try again.";
    try {
      const data = await res.json();
      if (typeof data.detail === "string") detail = data.detail;
    } catch {
      // response was not JSON, keep the default message
    }
    throw new Error(detail);
  }

  const data = await res.json();
  return data.response;
}