from huggingface_hub import InferenceClient

# 1. THE CREDENTIALS
HF_TOKEN = ""

# 2. THE SDK INITIALIZATION (Using Zephyr - an ungated, reliable model)
print("Initializing the SDK Client...")
client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_TOKEN)

# 3. THE DATA
prompt = "Context: HTML contains <button id='submit-2026'>. Task: What is the new ID? Return ONLY the ID."

def run_xray_test():
    print("Sending request to Hugging Face...")
    try:
        # The SDK automatically finds the right router endpoint for this model
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(messages, max_tokens=15)
        
        # Clean the output
        clean_id = response.choices[0].message.content.strip().split()[-1]
        print(f"\n✅ PIPELINE SUCCESS! The extracted ID is: {clean_id}")
        
    except Exception as e:
        print("\n❌ SDK FAILED! Here is the EXACT reason why:")
        print("========================================")
        # repr() forces Python to show the raw underlying error data
        print(repr(e))
        print("========================================")

run_xray_test()