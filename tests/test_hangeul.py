"""Comprehensive tests for the hangeul library."""

import pytest

import hangeul_jamo_py as hangeul


class TestValidation:
    """Tests for validation functions."""

    def test_is_hangul_syllable(self):
        """Test Hangul syllable detection."""
        # Valid Hangul syllables
        assert hangeul.is_hangul_syllable('가')
        assert hangeul.is_hangul_syllable('한')
        assert hangeul.is_hangul_syllable('글')
        assert hangeul.is_hangul_syllable('힣')

        # Invalid cases
        assert not hangeul.is_hangul_syllable('a')
        assert not hangeul.is_hangul_syllable('ㄱ')
        assert not hangeul.is_hangul_syllable('ㅏ')
        assert not hangeul.is_hangul_syllable('1')
        assert not hangeul.is_hangul_syllable(' ')

    def test_is_jamo(self):
        """Test jamo character detection."""
        # Valid jamo (U+11xx)
        assert hangeul.is_jamo('ᄀ')  # U+1100
        assert hangeul.is_jamo('ᅡ')  # U+1161
        assert hangeul.is_jamo('ᆨ')  # U+11A8

        # Invalid cases
        assert not hangeul.is_jamo('ㄱ')  # HCJ
        assert not hangeul.is_jamo('한')
        assert not hangeul.is_jamo('a')

    def test_is_hcj(self):
        """Test HCJ character detection."""
        # Valid HCJ
        assert hangeul.is_hcj('ㄱ')
        assert hangeul.is_hcj('ㅏ')
        assert hangeul.is_hcj('ㄲ')
        assert hangeul.is_hcj('ㅘ')

        # Invalid cases
        assert not hangeul.is_hcj('ᄀ')  # Jamo
        assert not hangeul.is_hcj('한')
        assert not hangeul.is_hcj('a')

    def test_is_jamo_lead(self):
        """Test leading consonant detection."""
        assert hangeul.is_jamo_lead('ㄱ')
        assert hangeul.is_jamo_lead('ㅎ')
        assert not hangeul.is_jamo_lead('ㅏ')
        assert not hangeul.is_jamo_lead('한')

    def test_is_jamo_vowel(self):
        """Test vowel detection."""
        assert hangeul.is_jamo_vowel('ㅏ')
        assert hangeul.is_jamo_vowel('ㅣ')
        assert not hangeul.is_jamo_vowel('ㄱ')
        assert not hangeul.is_jamo_vowel('한')

    def test_is_jamo_tail(self):
        """Test trailing consonant detection."""
        assert hangeul.is_jamo_tail('ㄱ')
        assert hangeul.is_jamo_tail('ㄴ')
        assert not hangeul.is_jamo_tail('ㅏ')
        assert not hangeul.is_jamo_tail('한')

    def test_is_jamo_compound(self):
        """Test compound jamo detection."""
        # Double consonants
        assert hangeul.is_jamo_compound('ㄲ')
        assert hangeul.is_jamo_compound('ㅆ')

        # Consonant clusters
        assert hangeul.is_jamo_compound('ㄳ')
        assert hangeul.is_jamo_compound('ㄺ')

        # Diphthongs
        assert hangeul.is_jamo_compound('ㅘ')
        assert hangeul.is_jamo_compound('ㅢ')

        # Non-compounds
        assert not hangeul.is_jamo_compound('ㄱ')
        assert not hangeul.is_jamo_compound('ㅏ')


class TestDecomposition:
    """Tests for decomposition functions."""

    def test_decompose_hcj(self):
        """Test text decomposition to HCJ."""
        # Basic decomposition
        assert hangeul.decompose_hcj('한글') == 'ㅎㅏㄴㄱㅡㄹ'
        assert hangeul.decompose_hcj('안녕하세요') == 'ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ'

        # Mixed text
        assert hangeul.decompose_hcj('Hello 한글!') == 'Hello ㅎㅏㄴㄱㅡㄹ!'

        # Empty and non-Hangul
        assert hangeul.decompose_hcj('') == ''
        assert hangeul.decompose_hcj('Hello') == 'Hello'
        assert hangeul.decompose_hcj('123') == '123'

    def test_decompose_compound(self):
        """Test compound jamo decomposition."""
        # Double consonants
        assert hangeul.decompose_compound('ㄲ') == ('ㄱ', 'ㄱ')
        assert hangeul.decompose_compound('ㄸ') == ('ㄷ', 'ㄷ')

        # Consonant clusters
        assert hangeul.decompose_compound('ㄳ') == ('ㄱ', 'ㅅ')
        assert hangeul.decompose_compound('ㄺ') == ('ㄹ', 'ㄱ')

        # Diphthongs
        assert hangeul.decompose_compound('ㅘ') == ('ㅗ', 'ㅏ')
        assert hangeul.decompose_compound('ㅢ') == ('ㅡ', 'ㅣ')

    def test_decompose_compound_invalid(self):
        """Test compound decomposition with invalid input."""
        with pytest.raises(hangeul.InvalidJamoError):
            hangeul.decompose_compound('ㄱ')

        with pytest.raises(hangeul.InvalidJamoError):
            hangeul.decompose_compound('한')


class TestComposition:
    """Tests for composition functions."""

    def test_compose_hcj(self):
        """Test HCJ text composition."""
        # Basic composition
        assert hangeul.compose_hcj('ㅎㅏㄴㄱㅡㄹ') == '한글'
        assert hangeul.compose_hcj('ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ') == '안녕하세요'

        # Mixed text
        assert hangeul.compose_hcj('Hello ㅎㅏㄴㄱㅡㄹ!') == 'Hello 한글!'

        # Edge cases
        assert hangeul.compose_hcj('') == ''
        assert hangeul.compose_hcj('Hello') == 'Hello'
        assert hangeul.compose_hcj('ㄱㄱ') == 'ㄱㄱ'  # No vowel
        assert hangeul.compose_hcj('ㅏㅏ') == 'ㅏㅏ'  # No consonant

    def test_compose_decompose_roundtrip(self):
        """Test that compose_hcj and decompose_hcj are inverses."""
        test_cases = ['한글', '안녕하세요', '대한민국', '가나다라마바사']

        for text in test_cases:
            decomposed = hangeul.decompose_hcj(text)
            recomposed = hangeul.compose_hcj(decomposed)
            assert recomposed == text

    def test_compose_compound(self):
        """Test compound jamo composition."""
        # Double consonants
        assert hangeul.compose_compound(('ㄱ', 'ㄱ')) == 'ㄲ'
        assert hangeul.compose_compound(['ㅅ', 'ㅅ']) == 'ㅆ'

        # Consonant clusters
        assert hangeul.compose_compound(('ㄱ', 'ㅅ')) == 'ㄳ'
        assert hangeul.compose_compound(['ㄹ', 'ㄱ']) == 'ㄺ'

        # Diphthongs
        assert hangeul.compose_compound(('ㅗ', 'ㅏ')) == 'ㅘ'
        assert hangeul.compose_compound(['ㅡ', 'ㅣ']) == 'ㅢ'

    def test_compose_compound_invalid(self):
        """Test compound composition with invalid input."""
        with pytest.raises(hangeul.InvalidJamoError):
            hangeul.compose_compound(('ㄱ', 'ㄴ'))

        with pytest.raises(hangeul.InvalidJamoError):
            hangeul.compose_compound(['ㅏ', 'ㅓ'])


class TestConversion:
    """Tests for conversion functions."""

    def test_jamo_to_hcj(self):
        """Test jamo to HCJ conversion."""
        # Leads
        assert hangeul.jamo_to_hcj('ᄀ') == 'ㄱ'
        assert hangeul.jamo_to_hcj('ᄒ') == 'ㅎ'

        # Vowels
        assert hangeul.jamo_to_hcj('ᅡ') == 'ㅏ'
        assert hangeul.jamo_to_hcj('ᅵ') == 'ㅣ'

        # Tails
        assert hangeul.jamo_to_hcj('ᆨ') == 'ㄱ'
        assert hangeul.jamo_to_hcj('ᆫ') == 'ㄴ'

        # Non-jamo (should return as-is)
        assert hangeul.jamo_to_hcj('a') == 'a'

    def test_hcj_to_jamo(self):
        """Test HCJ to jamo conversion."""
        # Leads
        assert hangeul.hcj_to_jamo('ㄱ', 'lead') == 'ᄀ'
        assert hangeul.hcj_to_jamo('ㅎ', 'lead') == 'ᄒ'

        # Vowels
        assert hangeul.hcj_to_jamo('ㅏ', 'vowel') == 'ᅡ'
        assert hangeul.hcj_to_jamo('ㅣ', 'vowel') == 'ᅵ'

        # Tails
        assert hangeul.hcj_to_jamo('ㄱ', 'tail') == 'ᆨ'
        assert hangeul.hcj_to_jamo('ㄴ', 'tail') == 'ᆫ'

    def test_hcj_to_jamo_invalid_position(self):
        """Test HCJ to jamo with invalid position."""
        with pytest.raises(hangeul.InvalidJamoError):
            hangeul.hcj_to_jamo('ㄱ', 'invalid')


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_first_and_last_syllables(self):
        """Test first and last Hangul syllables."""
        # First syllable: 가 (U+AC00)
        assert hangeul.decompose_hcj('가') == 'ㄱㅏ'

        # Last syllable: 힣 (U+D7A3)
        assert hangeul.decompose_hcj('힣') == 'ㅎㅣㅎ'

    def test_all_leads_vowels_tails(self):
        """Test composition with all possible jamo."""
        # Test a sample of all leads
        for lead in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅎ']:
            syllable = hangeul.compose_hcj(lead + 'ㅏ')
            assert hangeul.is_hangul_syllable(syllable)
            result = hangeul.decompose_hcj(syllable)
            assert result == lead + 'ㅏ'

    def test_unicode_properties(self):
        """Test that syllables are in the correct Unicode range."""
        syllable = hangeul.compose_hcj('ㅎㅏㄴ')
        codepoint = ord(syllable)
        assert 0xAC00 <= codepoint <= 0xD7A3

    def test_complex_text(self):
        """Test with complex real-world text."""
        text = '대한민국의 수도는 서울특별시입니다.'
        decomposed = hangeul.decompose_hcj(text)
        recomposed = hangeul.compose_hcj(decomposed)
        assert recomposed == text


class TestPerformance:
    """Performance-related tests."""

    def test_large_text_decomposition(self):
        """Test decomposition of large text."""
        text = '한글' * 1000
        result = hangeul.decompose_hcj(text)
        assert len(result) == 6000  # Each syllable becomes 3 characters

    def test_large_text_composition(self):
        """Test composition of large text."""
        text = 'ㅎㅏㄴㄱㅡㄹ' * 1000
        result = hangeul.compose_hcj(text)
        assert len(result) == 2000  # 6 jamo become 2 syllables


class TestConstants:
    """Tests for exported constants."""

    def test_jamo_constants(self):
        """Test that jamo constants are available."""
        assert len(hangeul.JAMO_LEADS) == 19
        assert len(hangeul.JAMO_VOWELS) == 21
        assert len(hangeul.JAMO_TAILS) == 28  # Including None

    def test_hcj_constants(self):
        """Test that HCJ constants are available."""
        assert len(hangeul.HCJ_LEADS) == 19
        assert len(hangeul.HCJ_VOWELS) == 21
        assert len(hangeul.HCJ_TAILS) == 28  # Including None

    def test_compound_constants(self):
        """Test that compound constants are available."""
        assert 'ㄲ' in hangeul.JAMO_COMPOUNDS
        assert 'ㅘ' in hangeul.JAMO_COMPOUNDS
        assert len(hangeul.JAMO_COMPOUNDS) > 0
