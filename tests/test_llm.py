from engine.llm_explainer import LLMExplainer


def main():

    print("\nStarting Qwen test...\n")

    llm = LLMExplainer()

    if not llm.is_available():
        print("❌ Qwen model is not available.")
        return

    print("✅ Qwen model is loaded.\n")

    response = llm.explain(
        query="I want PAN Card",
        document_name="PAN Card",
        category="Tax / Identity"
    )

    print("========================================")
    print("QWEN RESPONSE")
    print("========================================")
    print(response)
    print("========================================")


if __name__ == "__main__":
    main()