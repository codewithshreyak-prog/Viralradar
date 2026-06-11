import subprocess


steps = [
    ("Generating sample Reddit-style posts", "python scripts/generate_sample_posts.py"),
    ("Running sentiment analysis", "python -m viralradar.consumers.sentiment_analyzer"),
    ("Running viral spike detection", "python -m viralradar.detectors.spike_detector"),
]


def run_step(description, command):
    print(f"\n=== {description} ===")
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {description}")


if __name__ == "__main__":
    print("Starting ViralRadar pipeline...")

    for description, command in steps:
        run_step(description, command)

    print("\nViralRadar pipeline completed successfully!")
    print("Run dashboard with: python -m dashboard.app")
