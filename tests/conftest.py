"""Configuration commune des tests : une base SQLite jetable, jamais quizops.db."""

import os
import tempfile

os.environ["QUIZOPS_DB"] = os.path.join(
    tempfile.mkdtemp(prefix="quizops-tests-"), "test.db"
)
