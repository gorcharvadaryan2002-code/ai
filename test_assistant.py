import os
import tempfile
import unittest

from assistant import AssistantConfig, PersonalAssistant


class PersonalAssistantTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.assistant = PersonalAssistant(
            AssistantConfig(
                memory_file=self.tmp.name,
                ollama_base_url="",
                ollama_model="",
            )
        )

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_add_task(self):
        reply = self.assistant.respond("todo write sprint summary")
        self.assertIn("added this to your tasks", reply)

    def test_show_tasks(self):
        self.assistant.respond("todo file travel reimbursement")
        reply = self.assistant.respond("what are my tasks")
        self.assertIn("file travel reimbursement", reply)


if __name__ == "__main__":
    unittest.main()
