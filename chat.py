from harmonia import HarmoniaAgent


def main() -> None:
    agent = HarmoniaAgent(model="ri1-8b:latest")
    print("Harmonia LLM Agent connected to HarmoniaSystemIntegrator.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user.strip().lower() in {"exit", "quit"}:
            break

        reply = agent.step(user)
        print("HARMONIA:", reply)


if __name__ == "__main__":  # pragma: no cover
    main()
