import unittest
from tempfile import TemporaryDirectory

from lrc_compat import (
    APLAYER_TIMESTAMP_PATTERN,
    find_incompatible_lrc_timestamps,
    normalize_lrc_file,
    normalize_lrc_timestamps,
)


class LrcCompatTests(unittest.TestCase):
    def test_normalize_timestamps_to_aplayer_compatible_milliseconds(self):
        source = "\n".join(
            [
                "[00:01.8]one digit",
                "[3:5.4]short fields",
                "[01:15.979996]six digits",
                "[02:54.4]last line",
                "[03:00.04]already two digits",
                "[03:01.004]already three digits",
            ]
        )

        normalized = normalize_lrc_timestamps(source)

        self.assertIn("[00:01.800]one digit", normalized)
        self.assertIn("[03:05.400]short fields", normalized)
        self.assertIn("[01:15.980]six digits", normalized)
        self.assertIn("[02:54.400]last line", normalized)
        self.assertIn("[03:00.04]already two digits", normalized)
        self.assertIn("[03:01.004]already three digits", normalized)

    def test_normalized_timestamps_match_aplayer_parser_shape(self):
        normalized = normalize_lrc_timestamps(
            "[00:01.8]title\n"
            "[01:15.979996]line\n"
            "[02:54.4]tail"
        )

        for line in normalized.splitlines():
            timestamp = line.split("]", 1)[0] + "]"
            self.assertRegex(timestamp, APLAYER_TIMESTAMP_PATTERN)

    def test_reports_incompatible_timestamps_with_line_numbers(self):
        issues = find_incompatible_lrc_timestamps(
            "[00:01.8]bad\n"
            "[00:02.80]ok\n"
            "[00:03.1234]bad\n"
        )

        self.assertEqual(
            issues,
            [
                (1, "[00:01.8]"),
                (3, "[00:03.1234]"),
            ],
        )

    def test_normalize_file_preserves_existing_crlf_line_endings(self):
        with TemporaryDirectory() as tmpdir:
            path = f"{tmpdir}/song.lrc"
            with open(path, "wb") as handle:
                handle.write(b"[00:01.8]bad  \r\n[00:02.34]ok  \r\n")

            changed = normalize_lrc_file(path)

            self.assertTrue(changed)
            with open(path, "rb") as handle:
                self.assertEqual(
                    handle.read(),
                    b"[00:01.800]bad\r\n[00:02.34]ok  \r\n",
                )


if __name__ == "__main__":
    unittest.main()
