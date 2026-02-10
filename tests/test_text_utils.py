from techdocsbench.text_utils import clean_markdown


def test_clean_markdown_adds_blank_line_before_lists():
    text = "Вступление\n- пункт 1\n- пункт 2"
    result = clean_markdown(text)
    assert "Вступление\n\n- пункт 1" in result


def test_clean_markdown_preserves_code_blocks():
    text = "```\n- внутри кода\n```\n"
    result = clean_markdown(text)
    assert result.count("- внутри кода") == 1
