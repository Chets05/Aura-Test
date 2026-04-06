import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. THE CREDENTIALS
# We no longer hardcode tokens! We load them securely from the .env file
load_dotenv()

print("Initializing the NVIDIA NIM SDK Client...")

# 2. THE SDK INITIALIZATION (Using OpenAI standard for NVIDIA endpoints)
try:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API_KEY")
    )
except Exception as e:
    print("❌ Client Init Failed! Make sure your .env file is set up with NVIDIA_API_KEY.")
    exit(1)

# 3. THE DATA
# We use a strict system prompt and the exact test data your teammate provided
system_prompt = "You are a strict data parser. Return ONLY the requested ID string, nothing else."
user_prompt = "Context: HTML contains <button id='submit-2026'>. Task: What is the new ID? Return ONLY the ID."

def run_xray_test():
    print("Sending request to NVIDIA (Llama-3.1-70b-instruct)...")
    try:
        response = client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0, # 0.0 for strict deterministic output
            max_tokens=15
        )
        
        # Clean the output using the defensive logic we merged earlier
        raw_output = response.choices[0].message.content.strip()
        clean_id = raw_output.replace('"', '').replace("'", "").replace("`", "").split()[-1]
        
        print(f"\n✅ PIPELINE SUCCESS! The extracted ID is: {clean_id}")
        
    except Exception as e:
        print("\n❌ SDK FAILED! Here is the EXACT reason why:")
        print("========================================")
        # repr() forces Python to show the raw underlying error data
        print(repr(e))
        print("========================================")

if __name__ == "__main__":
    run_xray_test()