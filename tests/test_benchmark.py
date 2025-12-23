"""Performance benchmark tests for the hangeul library."""

import time
from typing import Callable

import pytest

import hangeul


class Timer:
    """Context manager for timing operations."""

    def __init__(self):
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start


def benchmark(func: Callable, iterations: int = 10000) -> float:
    """Benchmark a function and return average time per iteration.

    Args:
        func: Function to benchmark
        iterations: Number of iterations to run

    Returns:
        Average time per iteration in milliseconds
    """
    with Timer() as timer:
        for _ in range(iterations):
            func()

    return (timer.elapsed / iterations) * 1000  # Convert to ms


class TestDecompositionBenchmark:
    """Benchmark tests for decomposition operations."""

    def test_single_syllable_decomposition(self):
        """Benchmark single syllable decomposition."""
        iterations = 100000

        avg_time = benchmark(lambda: hangeul.decompose_hcj("한"), iterations)

        print(f"\n단일 음절 분해: {avg_time:.6f} ms/op ({iterations:,} iterations)")
        assert avg_time < 0.01, f"Too slow: {avg_time} ms"

    def test_short_text_decomposition(self):
        """Benchmark short text (5 syllables) decomposition."""
        text = "안녕하세요"
        iterations = 50000

        avg_time = benchmark(lambda: hangeul.decompose_hcj(text), iterations)

        print(
            f"\n짧은 텍스트 분해 (5자): {avg_time:.6f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 0.05, f"Too slow: {avg_time} ms"

    def test_medium_text_decomposition(self):
        """Benchmark medium text (50 syllables) decomposition."""
        text = "대한민국의 수도는 서울특별시입니다. 한글은 세계에서 가장 과학적인 문자입니다. 우리는 한글을 사랑합니다."
        iterations = 10000

        avg_time = benchmark(lambda: hangeul.decompose_hcj(text), iterations)

        print(
            f"\n중간 텍스트 분해 (50자): {avg_time:.6f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 0.5, f"Too slow: {avg_time} ms"

    def test_large_text_decomposition(self):
        """Benchmark large text (1000 syllables) decomposition."""
        text = "한글" * 500
        iterations = 1000

        avg_time = benchmark(lambda: hangeul.decompose_hcj(text), iterations)

        print(
            f"\n큰 텍스트 분해 (1000자): {avg_time:.6f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 10.0, f"Too slow: {avg_time} ms"

    def test_mixed_text_decomposition(self):
        """Benchmark mixed Korean-English text decomposition."""
        text = "Hello, 안녕하세요! This is a test. 이것은 테스트입니다."
        iterations = 20000

        avg_time = benchmark(lambda: hangeul.decompose_hcj(text), iterations)

        print(f"\n혼합 텍스트 분해: {avg_time:.6f} ms/op ({iterations:,} iterations)")
        assert avg_time < 0.1, f"Too slow: {avg_time} ms"


class TestCompositionBenchmark:
    """Benchmark tests for composition operations."""

    def test_single_syllable_composition(self):
        """Benchmark single syllable composition."""
        iterations = 100000

        avg_time = benchmark(lambda: hangeul.compose_hcj("ㅎㅏㄴ"), iterations)

        print(f"\n단일 음절 조합: {avg_time:.6f} ms/op ({iterations:,} iterations)")
        assert avg_time < 0.01, f"Too slow: {avg_time} ms"

    def test_short_text_composition(self):
        """Benchmark short text composition."""
        text = "ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ"
        iterations = 50000

        avg_time = benchmark(lambda: hangeul.compose_hcj(text), iterations)

        print(
            f"\n짧은 텍스트 조합 (5자): {avg_time:.6f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 0.05, f"Too slow: {avg_time} ms"

    def test_medium_text_composition(self):
        """Benchmark medium text composition."""
        text = hangeul.decompose_hcj(
            "대한민국의 수도는 서울특별시입니다. 한글은 세계에서 가장 과학적인 문자입니다."
        )
        iterations = 10000

        avg_time = benchmark(lambda: hangeul.compose_hcj(text), iterations)

        print(
            f"\n중간 텍스트 조합 (40자): {avg_time:.6f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 0.5, f"Too slow: {avg_time} ms"

    def test_large_text_composition(self):
        """Benchmark large text composition."""
        text = hangeul.decompose_hcj("한글" * 500)
        iterations = 1000

        avg_time = benchmark(lambda: hangeul.compose_hcj(text), iterations)

        print(
            f"\n큰 텍스트 조합 (1000자): {avg_time:.6f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 10.0, f"Too slow: {avg_time} ms"


class TestRoundTripBenchmark:
    """Benchmark tests for round-trip operations."""

    def test_short_text_roundtrip(self):
        """Benchmark short text round-trip (decompose + compose)."""
        text = "안녕하세요"
        iterations = 25000

        def roundtrip():
            decomposed = hangeul.decompose_hcj(text)
            hangeul.compose_hcj(decomposed)

        avg_time = benchmark(roundtrip, iterations)

        print(
            f"\n짧은 텍스트 왕복 (5자): {avg_time:.6f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 0.1, f"Too slow: {avg_time} ms"

    def test_medium_text_roundtrip(self):
        """Benchmark medium text round-trip."""
        text = "대한민국의 수도는 서울특별시입니다. 한글은 세계에서 가장 과학적인 문자입니다."
        iterations = 5000

        def roundtrip():
            decomposed = hangeul.decompose_hcj(text)
            hangeul.compose_hcj(decomposed)

        avg_time = benchmark(roundtrip, iterations)

        print(
            f"\n중간 텍스트 왕복 (40자): {avg_time:.6f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 1.0, f"Too slow: {avg_time} ms"


class TestValidationBenchmark:
    """Benchmark tests for validation operations."""

    def test_is_hangul_syllable(self):
        """Benchmark syllable validation."""
        iterations = 200000

        avg_time = benchmark(lambda: hangeul.is_hangul_syllable("한"), iterations)

        print(f"\n음절 검증: {avg_time:.6f} ms/op ({iterations:,} iterations)")
        assert avg_time < 0.005, f"Too slow: {avg_time} ms"

    def test_is_jamo(self):
        """Benchmark jamo validation."""
        iterations = 200000

        avg_time = benchmark(lambda: hangeul.is_jamo("ᄀ"), iterations)

        print(f"\n자모 검증: {avg_time:.6f} ms/op ({iterations:,} iterations)")
        assert avg_time < 0.005, f"Too slow: {avg_time} ms"

    def test_is_hcj(self):
        """Benchmark HCJ validation."""
        iterations = 200000

        avg_time = benchmark(lambda: hangeul.is_hcj("ㄱ"), iterations)

        print(f"\nHCJ 검증: {avg_time:.6f} ms/op ({iterations:,} iterations)")
        assert avg_time < 0.005, f"Too slow: {avg_time} ms"

    def test_is_jamo_compound(self):
        """Benchmark compound jamo validation."""
        iterations = 200000

        avg_time = benchmark(lambda: hangeul.is_jamo_compound("ㄲ"), iterations)

        print(f"\n복합 자모 검증: {avg_time:.6f} ms/op ({iterations:,} iterations)")
        assert avg_time < 0.005, f"Too slow: {avg_time} ms"


class TestCompoundJamoBenchmark:
    """Benchmark tests for compound jamo operations."""

    def test_decompose_compound(self):
        """Benchmark compound jamo decomposition."""
        iterations = 100000

        avg_time = benchmark(lambda: hangeul.decompose_compound("ㄲ"), iterations)

        print(f"\n복합 자모 분해: {avg_time:.6f} ms/op ({iterations:,} iterations)")
        assert avg_time < 0.01, f"Too slow: {avg_time} ms"

    def test_compose_compound(self):
        """Benchmark compound jamo composition."""
        iterations = 100000

        avg_time = benchmark(lambda: hangeul.compose_compound(("ㄱ", "ㄱ")), iterations)

        print(f"\n복합 자모 조합: {avg_time:.6f} ms/op ({iterations:,} iterations)")
        assert avg_time < 0.01, f"Too slow: {avg_time} ms"


class TestThroughput:
    """Test overall throughput of the library."""

    def test_decomposition_throughput(self):
        """Measure decomposition throughput (characters per second)."""
        text = "한글" * 10000  # 20,000 characters
        iterations = 100

        with Timer() as timer:
            for _ in range(iterations):
                hangeul.decompose_hcj(text)

        total_chars = len(text) * iterations
        chars_per_sec = total_chars / timer.elapsed

        print(f"\n분해 처리량: {chars_per_sec:,.0f} chars/sec")
        print(f"  ({total_chars:,} characters in {timer.elapsed:.2f} seconds)")

        assert chars_per_sec > 500_000, f"Too slow: {chars_per_sec:,.0f} chars/sec"

    def test_composition_throughput(self):
        """Measure composition throughput (characters per second)."""
        text = hangeul.decompose_hcj("한글" * 10000)  # ~60,000 jamo
        iterations = 100

        with Timer() as timer:
            for _ in range(iterations):
                hangeul.compose_hcj(text)

        total_chars = len(text) * iterations
        chars_per_sec = total_chars / timer.elapsed

        print(f"\n조합 처리량: {chars_per_sec:,.0f} chars/sec")
        print(f"  ({total_chars:,} characters in {timer.elapsed:.2f} seconds)")

        assert chars_per_sec > 500_000, f"Too slow: {chars_per_sec:,.0f} chars/sec"


class TestScalability:
    """Test how performance scales with input size."""

    def test_decomposition_scalability(self):
        """Test decomposition performance scaling."""
        sizes = [10, 100, 1000, 10000]
        results = []

        print("\n분해 성능 확장성:")
        for size in sizes:
            text = "한글" * (size // 2)
            iterations = max(1, 10000 // size)

            avg_time = benchmark(lambda: hangeul.decompose_hcj(text), iterations)
            time_per_char = avg_time / size

            results.append((size, avg_time, time_per_char))
            print(
                f"  {size:5d} chars: {avg_time:8.4f} ms total, {time_per_char:.6f} ms/char"
            )

        # Check that time per character remains roughly constant (O(n) complexity)
        first_time_per_char = results[0][2]
        last_time_per_char = results[-1][2]

        ratio = last_time_per_char / first_time_per_char
        print(f"  성능 비율 (마지막/첫번째): {ratio:.2f}x")

        assert ratio < 2.0, "Performance should scale linearly"

    def test_composition_scalability(self):
        """Test composition performance scaling."""
        sizes = [30, 300, 3000, 30000]  # Jamo counts
        results = []

        print("\n조합 성능 확장성:")
        for size in sizes:
            text = hangeul.decompose_hcj("한글" * (size // 6))
            iterations = max(1, 10000 // (size // 10))

            avg_time = benchmark(lambda: hangeul.compose_hcj(text), iterations)
            time_per_char = avg_time / size

            results.append((size, avg_time, time_per_char))
            print(
                f"  {size:5d} chars: {avg_time:8.4f} ms total, {time_per_char:.6f} ms/char"
            )

        # Check linear scaling
        first_time_per_char = results[0][2]
        last_time_per_char = results[-1][2]

        ratio = last_time_per_char / first_time_per_char
        print(f"  성능 비율 (마지막/첫번째): {ratio:.2f}x")

        assert ratio < 3.0, "Performance should scale roughly linearly"


class TestComparisonBenchmark:
    """Benchmark comparison with real-world scenarios."""

    def test_nlp_preprocessing_scenario(self):
        """Simulate NLP preprocessing scenario."""
        sentences = [
            "자연어 처리는 인공지능의 중요한 분야입니다.",
            "한국어는 교착어로 분류됩니다.",
            "형태소 분석은 한국어 처리의 기본입니다.",
            "딥러닝 기술이 자연어 처리를 혁신했습니다.",
            "챗봇은 자연어 이해 기술을 사용합니다.",
        ]

        iterations = 1000

        def preprocess():
            for sentence in sentences:
                # Decompose
                jamo = hangeul.decompose_hcj(sentence)
                # Analyze (simulated)
                _ = len(jamo)
                # Compose back
                hangeul.compose_hcj(jamo)

        avg_time = benchmark(preprocess, iterations)

        print(
            f"\nNLP 전처리 시나리오 (5 문장): {avg_time:.4f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 1.0, f"Too slow for NLP use: {avg_time} ms"

    def test_search_indexing_scenario(self):
        """Simulate search indexing scenario."""
        documents = ["한글" * 100] * 10  # 10 documents, 100 syllables each

        iterations = 100

        def index_documents():
            for doc in documents:
                # Decompose for indexing
                jamo = hangeul.decompose_hcj(doc)
                # Create terms (simulated)
                _ = set(jamo)

        avg_time = benchmark(index_documents, iterations)

        print(
            f"\n검색 인덱싱 시나리오 (10 문서): {avg_time:.4f} ms/op ({iterations:,} iterations)"
        )
        assert avg_time < 10.0, f"Too slow for indexing: {avg_time} ms"


if __name__ == "__main__":
    # Run benchmarks with verbose output
    pytest.main([__file__, "-v", "-s"])
