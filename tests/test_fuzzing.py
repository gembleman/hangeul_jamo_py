"""Fuzzing tests for hangeul library.

This module performs randomized fuzzing tests to verify 100% accuracy:
- Generates 10,000 random sentences, each containing 11,172 random Korean syllables
- Each sentence uses randomly selected syllables from all 11,172 possible Hangul characters
- Tests both HCJ and U+11xx jamo roundtrips
- Sentences are different on every test run (true fuzzing)
"""

import random
from typing import Generator

import pytest
from hangeul import (
    compose_hcj,
    compose_jamo,
    decompose_hcj,
    decompose_jamo,
)


def generate_random_hangul_text(length: int, seed: int | None = None) -> str:
    """Generate a random string of Hangul syllables.

    Args:
        length: Number of syllables to generate
        seed: Random seed for reproducibility (optional)

    Returns:
        String containing random Hangul syllables
    """
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()

    # All Hangul syllables: U+AC00 to U+D7A3 (11,172 total)
    syllables = [chr(code) for code in range(0xAC00, 0xD7A4)]

    return ''.join(rng.choice(syllables) for _ in range(length))


def generate_test_sentences(
    num_sentences: int = 10000,
    sentence_length: int = 11172,
) -> Generator[str, None, None]:
    """Generate random test sentences.

    Each sentence contains random Hangul syllables selected from all 11,172
    possible characters. The same character can appear consecutively.

    Args:
        num_sentences: Number of sentences to generate
        sentence_length: Length of each sentence in syllables

    Yields:
        Random Hangul sentences
    """
    for i in range(num_sentences):
        # Use different seed for each sentence to ensure variety
        yield generate_random_hangul_text(sentence_length)


class TestFuzzingHCJ:
    """Fuzzing tests for HCJ decompose/compose roundtrip."""

    def test_fuzzing_hcj_roundtrip_small_sample(self):
        """Test HCJ roundtrip with 100 random sentences (quick test)."""
        errors = []

        for idx, sentence in enumerate(generate_test_sentences(num_sentences=100, sentence_length=1000)):
            try:
                decomposed = decompose_hcj(sentence)
                recomposed = compose_hcj(decomposed)

                if recomposed != sentence:
                    errors.append(f"Sentence {idx}: Roundtrip mismatch")
                    # Show first difference
                    for i, (orig, recomp) in enumerate(zip(sentence, recomposed)):
                        if orig != recomp:
                            errors.append(f"  First diff at position {i}: {orig} != {recomp}")
                            break
                    if len(errors) >= 10:
                        break

            except Exception as e:
                errors.append(f"Sentence {idx}: {e}")
                if len(errors) >= 10:
                    break

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors)

    @pytest.mark.slow
    def test_fuzzing_hcj_roundtrip_full(self):
        """Test HCJ roundtrip with 10,000 random sentences of length 11,172.

        This is the full fuzzing test that covers all possible syllables.
        Run with: pytest -m slow
        """
        errors = []
        num_tested = 0

        for idx, sentence in enumerate(generate_test_sentences(num_sentences=10000, sentence_length=11172)):
            try:
                decomposed = decompose_hcj(sentence)
                recomposed = compose_hcj(decomposed)

                if recomposed != sentence:
                    errors.append(f"Sentence {idx}: Roundtrip mismatch")
                    # Show first difference
                    for i, (orig, recomp) in enumerate(zip(sentence, recomposed)):
                        if orig != recomp:
                            errors.append(f"  First diff at position {i}: {orig} != {recomp}")
                            break
                    if len(errors) >= 10:
                        break

                num_tested += 1

                # Progress indicator
                if (idx + 1) % 1000 == 0:
                    print(f"\rTested {idx + 1}/10000 sentences...", end="", flush=True)

            except Exception as e:
                errors.append(f"Sentence {idx}: {e}")
                if len(errors) >= 10:
                    break

        print(f"\rCompleted: {num_tested} sentences tested successfully")
        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors)


class TestFuzzingJamo:
    """Fuzzing tests for U+11xx jamo decompose/compose roundtrip."""

    def test_fuzzing_jamo_roundtrip_small_sample(self):
        """Test U+11xx jamo roundtrip with 100 random sentences (quick test)."""
        errors = []

        for idx, sentence in enumerate(generate_test_sentences(num_sentences=100, sentence_length=1000)):
            try:
                decomposed = decompose_jamo(sentence)
                recomposed = compose_jamo(decomposed)

                if recomposed != sentence:
                    errors.append(f"Sentence {idx}: Roundtrip mismatch")
                    # Show first difference
                    for i, (orig, recomp) in enumerate(zip(sentence, recomposed)):
                        if orig != recomp:
                            errors.append(f"  First diff at position {i}: {orig} != {recomp}")
                            break
                    if len(errors) >= 10:
                        break

            except Exception as e:
                errors.append(f"Sentence {idx}: {e}")
                if len(errors) >= 10:
                    break

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors)

    @pytest.mark.slow
    def test_fuzzing_jamo_roundtrip_full(self):
        """Test U+11xx jamo roundtrip with 10,000 random sentences of length 11,172.

        This is the full fuzzing test that covers all possible syllables.
        Run with: pytest -m slow
        """
        errors = []
        num_tested = 0

        for idx, sentence in enumerate(generate_test_sentences(num_sentences=10000, sentence_length=11172)):
            try:
                decomposed = decompose_jamo(sentence)
                recomposed = compose_jamo(decomposed)

                if recomposed != sentence:
                    errors.append(f"Sentence {idx}: Roundtrip mismatch")
                    # Show first difference
                    for i, (orig, recomp) in enumerate(zip(sentence, recomposed)):
                        if orig != recomp:
                            errors.append(f"  First diff at position {i}: {orig} != {recomp}")
                            break
                    if len(errors) >= 10:
                        break

                num_tested += 1

                # Progress indicator
                if (idx + 1) % 1000 == 0:
                    print(f"\rTested {idx + 1}/10000 sentences...", end="", flush=True)

            except Exception as e:
                errors.append(f"Sentence {idx}: {e}")
                if len(errors) >= 10:
                    break

        print(f"\rCompleted: {num_tested} sentences tested successfully")
        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors)


class TestFuzzingCombined:
    """Combined fuzzing tests for both HCJ and U+11xx jamo."""

    def test_fuzzing_both_formats_small_sample(self):
        """Test both formats with 100 random sentences (quick test)."""
        errors = []

        for idx, sentence in enumerate(generate_test_sentences(num_sentences=100, sentence_length=1000)):
            try:
                # Test HCJ
                decomposed_hcj = decompose_hcj(sentence)
                recomposed_hcj = compose_hcj(decomposed_hcj)

                if recomposed_hcj != sentence:
                    errors.append(f"Sentence {idx} HCJ: Roundtrip mismatch")

                # Test U+11xx jamo
                decomposed_jamo = decompose_jamo(sentence)
                recomposed_jamo = compose_jamo(decomposed_jamo)

                if recomposed_jamo != sentence:
                    errors.append(f"Sentence {idx} Jamo: Roundtrip mismatch")

                if len(errors) >= 10:
                    break

            except Exception as e:
                errors.append(f"Sentence {idx}: {e}")
                if len(errors) >= 10:
                    break

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors)

    @pytest.mark.slow
    def test_fuzzing_both_formats_full(self):
        """Test both formats with 10,000 random sentences of length 11,172.

        This is the ultimate fuzzing test that covers all possible syllables
        with both decomposition formats.
        Run with: pytest -m slow
        """
        errors = []
        num_tested = 0

        for idx, sentence in enumerate(generate_test_sentences(num_sentences=10000, sentence_length=11172)):
            try:
                # Test HCJ
                decomposed_hcj = decompose_hcj(sentence)
                recomposed_hcj = compose_hcj(decomposed_hcj)

                if recomposed_hcj != sentence:
                    errors.append(f"Sentence {idx} HCJ: Roundtrip mismatch")
                    if len(errors) >= 10:
                        break

                # Test U+11xx jamo
                decomposed_jamo = decompose_jamo(sentence)
                recomposed_jamo = compose_jamo(decomposed_jamo)

                if recomposed_jamo != sentence:
                    errors.append(f"Sentence {idx} Jamo: Roundtrip mismatch")
                    if len(errors) >= 10:
                        break

                num_tested += 1

                # Progress indicator
                if (idx + 1) % 1000 == 0:
                    print(f"\rTested {idx + 1}/10000 sentences (both formats)...", end="", flush=True)

            except Exception as e:
                errors.append(f"Sentence {idx}: {e}")
                if len(errors) >= 10:
                    break

        print(f"\rCompleted: {num_tested} sentences tested successfully with both formats")
        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors)


class TestFuzzingStatistics:
    """Statistical analysis of fuzzing test coverage."""

    def test_syllable_distribution_coverage(self):
        """Verify that fuzzing covers a good distribution of all syllables."""
        # Generate a large sample
        all_chars = set()

        for sentence in generate_test_sentences(num_sentences=100, sentence_length=1000):
            all_chars.update(sentence)

        # We should see a significant portion of all possible syllables
        total_possible = 11172
        coverage = len(all_chars)
        coverage_percent = (coverage / total_possible) * 100

        print(f"\nSyllable coverage: {coverage}/{total_possible} ({coverage_percent:.2f}%)")

        # With 100 sentences of 1000 chars each, we should see at least 50% coverage
        assert coverage_percent >= 50, f"Coverage too low: {coverage_percent:.2f}%"

    def test_consecutive_same_characters(self):
        """Verify that same characters can appear consecutively."""
        found_consecutive = False

        for sentence in generate_test_sentences(num_sentences=10, sentence_length=1000):
            for i in range(len(sentence) - 1):
                if sentence[i] == sentence[i + 1]:
                    found_consecutive = True
                    break
            if found_consecutive:
                break

        assert found_consecutive, "Should find consecutive same characters in random text"

    def test_randomness_verification(self):
        """Verify that generated sentences are different each time."""
        sentences = [
            generate_random_hangul_text(100)
            for _ in range(10)
        ]

        # All sentences should be different
        unique_sentences = set(sentences)
        assert len(unique_sentences) == 10, "Generated sentences should all be different"


class TestFuzzingEdgeCases:
    """Test edge cases with random data."""

    def test_short_random_texts(self):
        """Test with very short random texts."""
        errors = []

        for length in [1, 2, 3, 5, 10]:
            for _ in range(100):
                text = generate_random_hangul_text(length)

                try:
                    # HCJ roundtrip
                    assert compose_hcj(decompose_hcj(text)) == text

                    # Jamo roundtrip
                    assert compose_jamo(decompose_jamo(text)) == text

                except Exception as e:
                    errors.append(f"Length {length}, text '{text}': {e}")
                    if len(errors) >= 10:
                        break

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors)

    def test_medium_random_texts(self):
        """Test with medium-length random texts."""
        errors = []

        for _ in range(1000):
            length = random.randint(50, 500)
            text = generate_random_hangul_text(length)

            try:
                # HCJ roundtrip
                assert compose_hcj(decompose_hcj(text)) == text

                # Jamo roundtrip
                assert compose_jamo(decompose_jamo(text)) == text

            except Exception as e:
                errors.append(f"Length {length}: {e}")
                if len(errors) >= 10:
                    break

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors)
