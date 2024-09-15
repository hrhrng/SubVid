import pytest
import os
from src.subvid.main import extract_audio, transcribe_audio, format_time, create_srt

def test_extract_audio(tmp_path):
    # Create a dummy video file
    dummy_video = tmp_path / "dummy_video.mp4"
    dummy_video.write_bytes(b"dummy video content")

    audio_path = extract_audio(str(dummy_video))
    assert os.path.exists(audio_path)
    assert audio_path.endswith(".wav")

    # Clean up
    os.remove(audio_path)

def test_transcribe_audio(mocker):
    mock_model = mocker.Mock()
    mock_model.transcribe.return_value = {"segments": [{"start": 0, "end": 1, "text": "Test transcription"}]}
    mocker.patch("whisper.load_model", return_value=mock_model)

    result = transcribe_audio("dummy_audio.wav")
    assert len(result) == 1
    assert result[0]["text"] == "Test transcription"

def test_format_time():
    assert format_time(3661.5) == "01:01:01,500"
    assert format_time(0) == "00:00:00,000"
    assert format_time(59.999) == "00:00:59,999"

def test_create_srt(tmp_path):
    segments = [
        {"start": 0, "end": 1, "text": "Hello"},
        {"start": 1, "end": 2, "text": "World"}
    ]
    output_path = tmp_path / "test_subtitles.srt"
    create_srt(segments, str(output_path))

    assert output_path.exists()
    content = output_path.read_text()
    expected_content = "1\n00:00:00,000 --> 00:00:01,000\nHello\n\n2\n00:00:01,000 --> 00:00:02,000\nWorld\n\n"
    assert content == expected_content