"""Basic usage examples for the Hangeul library."""

import io
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import hangeul


def main():
    """Demonstrate basic Hangeul library features."""
    print("=" * 60)
    print("Hangeul Library - Basic Usage Examples")
    print("=" * 60)
    print()

    # Example 1: Decomposing text
    print("1. Decomposing Hangul text")
    print("-" * 40)
    text = "안녕하세요"
    decomposed = hangeul.decompose_hcj(text)
    print(f"Original:    {text}")
    print(f"Decomposed:  {decomposed}")
    print()

    # Example 2: Composing text
    print("2. Composing jamo into syllables")
    print("-" * 40)
    jamo_text = "ㅎㅏㄴㄱㅡㄹ"
    composed = hangeul.compose_hcj(jamo_text)
    print(f"Jamo:        {jamo_text}")
    print(f"Composed:    {composed}")
    print()

    # Example 3: Round-trip conversion
    print("3. Round-trip conversion")
    print("-" * 40)
    original = "대한민국"
    step1 = hangeul.decompose_hcj(original)
    step2 = hangeul.compose_hcj(step1)
    print(f"Original:    {original}")
    print(f"Decomposed:  {step1}")
    print(f"Recomposed:  {step2}")
    print(f"Match:       {original == step2}")
    print()

    # Example 4: Working with mixed text
    print("4. Working with mixed text")
    print("-" * 40)
    mixed = "Hello, 한글! How are you?"
    print(f"Original:    {mixed}")
    print(f"Decomposed:  {hangeul.decompose_hcj(mixed)}")
    print()

    # Example 7: Compound jamo
    print("7. Compound jamo decomposition")
    print("-" * 40)
    compounds = ["ㄲ", "ㅘ", "ㄺ"]
    for compound in compounds:
        components = hangeul.decompose_compound(compound)
        print(f"{compound} → {' + '.join(components)}")
    print()

    # Example 8: Validation
    print("8. Character validation")
    print("-" * 40)
    test_chars = ["한", "ㄱ", "ㅏ", "a", "ᄀ"]
    for char in test_chars:
        is_syllable = hangeul.is_hangul_syllable(char)
        is_hcj_char = hangeul.is_hcj(char)
        is_jamo_char = hangeul.is_jamo(char)
        print(
            f"'{char}' - Syllable: {is_syllable}, HCJ: {is_hcj_char}, Jamo: {is_jamo_char}"
        )
    print()

    # Example 10: Real-world example
    print("10. Real-world example: Text analysis")
    print("-" * 40)
    sentence = "Python으로 한글을 처리합니다."
    decomposed = hangeul.decompose_hcj(sentence)

    # Count unique jamo
    jamo_chars = [c for c in decomposed if hangeul.is_hcj(c)]
    unique_jamo = set(jamo_chars)

    print(f"Sentence:     {sentence}")
    print(f"Total jamo:   {len(jamo_chars)}")
    print(f"Unique jamo:  {len(unique_jamo)}")
    print(f"Jamo set:     {' '.join(sorted(unique_jamo))}")
    print()

    print("=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
