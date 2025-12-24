"""Comprehensive tests for hangeul library.

This module tests 100% of all valid Korean syllable and jamo combinations:
- All 11,172 Korean syllables (U+AC00 to U+D7A3)
- All 19 leading consonants (초성)
- All 21 vowels (중성)
- All 27 trailing consonants (종성)
- All compound jamo (double consonants, clusters, diphthongs)
- Edge cases and error conditions
"""

import pytest
from hangeul_jamo_py import (
    compose_compound,
    compose_hcj,
    compose_jamo,
    decompose_compound,
    decompose_hcj,
    decompose_jamo,
    hcj_to_jamo,
    is_hangul_syllable,
    is_hcj,
    is_jamo,
    is_jamo_compound,
    is_jamo_lead,
    is_jamo_tail,
    is_jamo_vowel,
    jamo_to_hcj,
    HCJ_LEADS,
    HCJ_VOWELS,
    HCJ_TAILS,
    JAMO_COMPOUNDS,
    InvalidJamoError,
)


class TestAllHangulSyllables:
    """Test all 11,172 Korean syllables."""

    def test_all_syllables_decompose_hcj(self):
        """Test that all 11,172 Hangul syllables can be decomposed to HCJ."""
        errors = []

        for code in range(0xAC00, 0xD7A4):
            syllable = chr(code)
            try:
                decomposed = decompose_hcj(syllable)

                # Verify decomposed result
                assert len(decomposed) in (2, 3), f"Syllable {syllable} decomposed to {len(decomposed)} jamo"
                assert all(is_hcj(c) for c in decomposed), f"Not all HCJ in {decomposed} from {syllable}"

            except Exception as e:
                errors.append(f"Failed to decompose {syllable} (U+{code:04X}): {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_syllables_decompose_jamo(self):
        """Test that all 11,172 Hangul syllables can be decomposed to U+11xx jamo."""
        errors = []

        for code in range(0xAC00, 0xD7A4):
            syllable = chr(code)
            try:
                decomposed = decompose_jamo(syllable)

                # Verify decomposed result
                assert len(decomposed) in (2, 3), f"Syllable {syllable} decomposed to {len(decomposed)} jamo"
                assert all(is_jamo(c) for c in decomposed), f"Not all jamo in {decomposed} from {syllable}"

            except Exception as e:
                errors.append(f"Failed to decompose {syllable} (U+{code:04X}): {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_syllables_roundtrip_hcj(self):
        """Test that all syllables can be decomposed and recomposed via HCJ."""
        errors = []

        for code in range(0xAC00, 0xD7A4):
            original = chr(code)
            try:
                decomposed = decompose_hcj(original)
                recomposed = compose_hcj(decomposed)

                assert recomposed == original, \
                    f"Roundtrip failed: {original} -> {decomposed} -> {recomposed}"

            except Exception as e:
                errors.append(f"Roundtrip failed for {original} (U+{code:04X}): {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_syllables_roundtrip_jamo(self):
        """Test that all syllables can be decomposed and recomposed via U+11xx jamo."""
        errors = []

        for code in range(0xAC00, 0xD7A4):
            original = chr(code)
            try:
                decomposed = decompose_jamo(original)
                recomposed = compose_jamo(decomposed)

                assert recomposed == original, \
                    f"Roundtrip failed: {original} -> {decomposed} -> {recomposed}"

            except Exception as e:
                errors.append(f"Roundtrip failed for {original} (U+{code:04X}): {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])


class TestAllJamoCombinations:
    """Test all valid jamo combinations."""

    def test_all_lead_vowel_combinations(self):
        """Test all 19*21 = 399 lead+vowel combinations."""
        errors = []

        for lead in HCJ_LEADS:
            for vowel in HCJ_VOWELS:
                jamo_str = lead + vowel
                try:
                    syllable = compose_hcj(jamo_str)

                    # Verify it's a valid syllable
                    assert len(syllable) == 1, f"Expected 1 char, got {len(syllable)}"
                    assert is_hangul_syllable(syllable), f"{syllable} is not a Hangul syllable"

                    # Verify roundtrip
                    decomposed = decompose_hcj(syllable)
                    assert decomposed == jamo_str, \
                        f"Roundtrip failed: {jamo_str} -> {syllable} -> {decomposed}"

                except Exception as e:
                    errors.append(f"Failed for {jamo_str}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_lead_vowel_tail_combinations(self):
        """Test all 19*21*27 = 10,773 lead+vowel+tail combinations."""
        errors = []

        for lead in HCJ_LEADS:
            for vowel in HCJ_VOWELS:
                for tail in HCJ_TAILS:
                    if tail is None:
                        continue

                    jamo_str = lead + vowel + tail
                    try:
                        syllable = compose_hcj(jamo_str)

                        # Verify it's a valid syllable
                        assert len(syllable) == 1, f"Expected 1 char, got {len(syllable)}"
                        assert is_hangul_syllable(syllable), f"{syllable} is not a Hangul syllable"

                        # Verify roundtrip
                        decomposed = decompose_hcj(syllable)
                        assert decomposed == jamo_str, \
                            f"Roundtrip failed: {jamo_str} -> {syllable} -> {decomposed}"

                    except Exception as e:
                        errors.append(f"Failed for {jamo_str}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])


class TestAllCompoundJamo:
    """Test all compound jamo (double consonants, clusters, diphthongs)."""

    def test_all_compound_decomposition(self):
        """Test decomposition of all compound jamo."""
        errors = []

        for compound, components in JAMO_COMPOUNDS.items():
            try:
                result = decompose_compound(compound)
                assert result == components, \
                    f"Expected {components}, got {result} for {compound}"

            except Exception as e:
                errors.append(f"Failed to decompose {compound}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_compound_composition(self):
        """Test composition of all compound jamo."""
        errors = []

        for compound, components in JAMO_COMPOUNDS.items():
            try:
                result = compose_compound(components)
                assert result == compound, \
                    f"Expected {compound}, got {result} from {components}"

            except Exception as e:
                errors.append(f"Failed to compose {components}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_compound_roundtrip(self):
        """Test roundtrip for all compound jamo."""
        errors = []

        for compound in JAMO_COMPOUNDS.keys():
            try:
                components = decompose_compound(compound)
                recomposed = compose_compound(components)
                assert recomposed == compound, \
                    f"Roundtrip failed: {compound} -> {components} -> {recomposed}"

            except Exception as e:
                errors.append(f"Roundtrip failed for {compound}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])


class TestJamoValidation:
    """Test validation functions for all jamo types."""

    def test_all_hcj_leads_validation(self):
        """Test that all HCJ leads are correctly validated."""
        for lead in HCJ_LEADS:
            assert is_hcj(lead), f"{lead} should be recognized as HCJ"
            assert is_jamo_lead(lead), f"{lead} should be recognized as lead jamo"

    def test_all_hcj_vowels_validation(self):
        """Test that all HCJ vowels are correctly validated."""
        for vowel in HCJ_VOWELS:
            assert is_hcj(vowel), f"{vowel} should be recognized as HCJ"
            assert is_jamo_vowel(vowel), f"{vowel} should be recognized as vowel jamo"

    def test_all_hcj_tails_validation(self):
        """Test that all HCJ tails are correctly validated."""
        for tail in HCJ_TAILS:
            if tail is None:
                continue
            assert is_hcj(tail), f"{tail} should be recognized as HCJ"
            assert is_jamo_tail(tail), f"{tail} should be recognized as tail jamo"

    def test_all_compound_validation(self):
        """Test that all compound jamo are correctly validated."""
        for compound in JAMO_COMPOUNDS.keys():
            assert is_jamo_compound(compound), \
                f"{compound} should be recognized as compound jamo"


class TestJamoConversion:
    """Test conversion between U+11xx jamo and HCJ."""

    def test_all_jamo_to_hcj_leads(self):
        """Test conversion of all leading jamo to HCJ."""
        errors = []

        for i, hcj_lead in enumerate(HCJ_LEADS):
            jamo_lead = chr(0x1100 + i)
            try:
                converted = jamo_to_hcj(jamo_lead)
                assert converted == hcj_lead, \
                    f"Expected {hcj_lead}, got {converted} from {jamo_lead}"

            except Exception as e:
                errors.append(f"Failed to convert {jamo_lead}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_jamo_to_hcj_vowels(self):
        """Test conversion of all vowel jamo to HCJ."""
        errors = []

        for i, hcj_vowel in enumerate(HCJ_VOWELS):
            jamo_vowel = chr(0x1161 + i)
            try:
                converted = jamo_to_hcj(jamo_vowel)
                assert converted == hcj_vowel, \
                    f"Expected {hcj_vowel}, got {converted} from {jamo_vowel}"

            except Exception as e:
                errors.append(f"Failed to convert {jamo_vowel}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_jamo_to_hcj_tails(self):
        """Test conversion of all trailing jamo to HCJ."""
        errors = []

        for i, hcj_tail in enumerate(HCJ_TAILS[1:]):  # Skip None
            jamo_tail = chr(0x11A8 + i)
            try:
                converted = jamo_to_hcj(jamo_tail)
                assert converted == hcj_tail, \
                    f"Expected {hcj_tail}, got {converted} from {jamo_tail}"

            except Exception as e:
                errors.append(f"Failed to convert {jamo_tail}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_hcj_to_jamo_leads(self):
        """Test conversion of all HCJ leads to jamo."""
        errors = []

        for i, hcj_lead in enumerate(HCJ_LEADS):
            jamo_lead = chr(0x1100 + i)
            try:
                converted = hcj_to_jamo(hcj_lead, "lead")
                assert converted == jamo_lead, \
                    f"Expected {jamo_lead}, got {converted} from {hcj_lead}"

            except Exception as e:
                errors.append(f"Failed to convert {hcj_lead}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_hcj_to_jamo_vowels(self):
        """Test conversion of all HCJ vowels to jamo."""
        errors = []

        for i, hcj_vowel in enumerate(HCJ_VOWELS):
            jamo_vowel = chr(0x1161 + i)
            try:
                converted = hcj_to_jamo(hcj_vowel, "vowel")
                assert converted == jamo_vowel, \
                    f"Expected {jamo_vowel}, got {converted} from {hcj_vowel}"

            except Exception as e:
                errors.append(f"Failed to convert {hcj_vowel}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])

    def test_all_hcj_to_jamo_tails(self):
        """Test conversion of all HCJ tails to jamo."""
        errors = []

        for i, hcj_tail in enumerate(HCJ_TAILS[1:]):  # Skip None
            jamo_tail = chr(0x11A8 + i)
            try:
                converted = hcj_to_jamo(hcj_tail, "tail")
                assert converted == jamo_tail, \
                    f"Expected {jamo_tail}, got {converted} from {hcj_tail}"

            except Exception as e:
                errors.append(f"Failed to convert {hcj_tail}: {e}")

        assert not errors, f"Found {len(errors)} errors:\n" + "\n".join(errors[:10])


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_string_decompose_hcj(self):
        """Test decompose_hcj with empty string."""
        assert decompose_hcj("") == ""

    def test_empty_string_decompose_jamo(self):
        """Test decompose_jamo with empty string."""
        assert decompose_jamo("") == ""

    def test_empty_string_compose_hcj(self):
        """Test compose_hcj with empty string."""
        assert compose_hcj("") == ""

    def test_empty_string_compose_jamo(self):
        """Test compose_jamo with empty string."""
        assert compose_jamo("") == ""

    def test_non_hangul_passthrough_decompose_hcj(self):
        """Test that non-Hangul characters pass through unchanged."""
        text = "Hello 123 !@# "
        assert decompose_hcj(text) == text

    def test_non_hangul_passthrough_decompose_jamo(self):
        """Test that non-Hangul characters pass through unchanged."""
        text = "Hello 123 !@# "
        assert decompose_jamo(text) == text

    def test_non_hangul_passthrough_compose_hcj(self):
        """Test that non-Hangul characters pass through unchanged."""
        text = "Hello 123 !@# "
        assert compose_hcj(text) == text

    def test_non_hangul_passthrough_compose_jamo(self):
        """Test that non-Hangul characters pass through unchanged."""
        text = "Hello 123 !@# "
        assert compose_jamo(text) == text

    def test_mixed_content_decompose_hcj(self):
        """Test decompose_hcj with mixed Korean and non-Korean content."""
        result = decompose_hcj("Hello 한글 World 테스트!")
        assert "Hello" in result
        assert "World" in result
        assert "!" in result
        # Korean parts should be decomposed
        assert "한" not in result
        assert "글" not in result
        assert "테" not in result
        assert "스" not in result
        assert "트" not in result

    def test_mixed_content_compose_hcj(self):
        """Test compose_hcj with mixed content."""
        decomposed = "Hello ㅎㅏㄴㄱㅡㄹ World"
        result = compose_hcj(decomposed)
        assert result == "Hello 한글 World"

    def test_invalid_compound_decompose(self):
        """Test decompose_compound with invalid jamo."""
        with pytest.raises(InvalidJamoError):
            decompose_compound("ㄱ")

    def test_invalid_compound_compose(self):
        """Test compose_compound with invalid components."""
        with pytest.raises(InvalidJamoError):
            compose_compound(("ㄱ", "ㄴ", "ㄷ"))

    def test_incomplete_syllable_composition(self):
        """Test that incomplete syllables are not composed."""
        # Just a consonant
        assert compose_hcj("ㄱ") == "ㄱ"
        # Just a vowel
        assert compose_hcj("ㅏ") == "ㅏ"

    def test_lookahead_in_composition(self):
        """Test that lookahead works correctly in composition."""
        # ㄱㅏㄴㅏ should be 가나, not 간ㅏ
        assert compose_hcj("ㄱㅏㄴㅏ") == "가나"
        # ㄱㅏㄴㄱㅏ should be 간가, not 가ㄴ가
        assert compose_hcj("ㄱㅏㄴㄱㅏ") == "간가"

    def test_long_text_roundtrip(self):
        """Test roundtrip with a long text containing all syllable types."""
        original = "가나다라마바사아자차카타파하" * 100
        decomposed = decompose_hcj(original)
        recomposed = compose_hcj(decomposed)
        assert recomposed == original

    def test_all_syllable_types_in_text(self):
        """Test text with syllables of different structures."""
        # 가: ㄱ+ㅏ (no tail)
        # 간: ㄱ+ㅏ+ㄴ (simple tail)
        # 값: ㄱ+ㅏ+ㅄ (compound tail)
        text = "가간값"

        # HCJ roundtrip
        decomposed_hcj = decompose_hcj(text)
        assert compose_hcj(decomposed_hcj) == text

        # Jamo roundtrip
        decomposed_jamo = decompose_jamo(text)
        assert compose_jamo(decomposed_jamo) == text


class TestRealWorldExamples:
    """Test with real-world Korean text examples."""

    def test_common_phrases(self):
        """Test common Korean phrases."""
        phrases = [
            "안녕하세요",
            "감사합니다",
            "죄송합니다",
            "사랑해요",
            "고맙습니다",
            "괜찮아요",
            "이해했어요",
            "모르겠어요",
            "힘내세요",
            "축하합니다",
        ]

        for phrase in phrases:
            # HCJ roundtrip
            decomposed_hcj = decompose_hcj(phrase)
            recomposed_hcj = compose_hcj(decomposed_hcj)
            assert recomposed_hcj == phrase, f"HCJ roundtrip failed for: {phrase}"

            # Jamo roundtrip
            decomposed_jamo = decompose_jamo(phrase)
            recomposed_jamo = compose_jamo(decomposed_jamo)
            assert recomposed_jamo == phrase, f"Jamo roundtrip failed for: {phrase}"

    def test_mixed_korean_english(self):
        """Test text with mixed Korean and English."""
        text = "Hello, 안녕하세요! This is a test 테스트입니다."

        # HCJ roundtrip
        decomposed_hcj = decompose_hcj(text)
        recomposed_hcj = compose_hcj(decomposed_hcj)
        assert recomposed_hcj == text

        # Jamo roundtrip
        decomposed_jamo = decompose_jamo(text)
        recomposed_jamo = compose_jamo(decomposed_jamo)
        assert recomposed_jamo == text

    def test_all_jamo_types_in_word(self):
        """Test words containing various jamo types."""
        # 닭: ㄷ+ㅏ+ㄺ (consonant cluster tail)
        # 없: ㅇ+ㅓ+ㅄ (consonant cluster tail)
        # 꽃: ㄲ+ㅗ+ㅊ (double consonant lead)
        words = ["닭", "없", "꽃", "짧", "넓", "핥"]

        for word in words:
            # HCJ roundtrip
            decomposed_hcj = decompose_hcj(word)
            recomposed_hcj = compose_hcj(decomposed_hcj)
            assert recomposed_hcj == word, f"HCJ roundtrip failed for: {word}"

            # Jamo roundtrip
            decomposed_jamo = decompose_jamo(word)
            recomposed_jamo = compose_jamo(decomposed_jamo)
            assert recomposed_jamo == word, f"Jamo roundtrip failed for: {word}"
