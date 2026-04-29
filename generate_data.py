import random
import os


def generate_dna(length):
    return ''.join(random.choice("ACGT") for _ in range(length))


def mutate_pattern(pattern, k):
    pattern = list(pattern)
    positions = random.sample(range(len(pattern)), k)

    for pos in positions:
        old_char = pattern[pos]
        choices = [c for c in "ACGT" if c != old_char]
        pattern[pos] = random.choice(choices)

    return ''.join(pattern)


def find_matches(text, pattern, k):
    n = len(text)
    m = len(pattern)
    result = []

    for i in range(n - m + 1):
        mismatch = 0
        for j in range(m):
            if text[i + j] != pattern[j]:
                mismatch += 1
                if mismatch > k:
                    break
        if mismatch <= k:
            result.append(i)

    return result


def save_test_cases():
    lengths = [10, 20, 40, 80, 160, 320, 640, 1280]
    output_dir = "dataset/artificial data"

    os.makedirs(output_dir, exist_ok=True)

    for length in lengths:
        file_path = os.path.join(output_dir, f"dna_{length}.txt")

        with open(file_path, "w") as f:
            for _ in range(10):
                text = generate_dna(length)

                pattern_len = max(3, length // 10)
                start = random.randint(0, length - pattern_len)

                original_pattern = text[start:start + pattern_len]

                k = random.randint(0, max(1, pattern_len // 3))

                pattern = mutate_pattern(original_pattern, k)

                output = find_matches(text, pattern, k)

                f.write(f"{text} {pattern} {k} {output}\n")

        print(f"Saved {file_path}")


if __name__ == "__main__":
    save_test_cases()