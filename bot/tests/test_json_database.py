"""Unit tests for JSON file-based database.

USAGE: cd bot, then python -m pytest tests/test_json_database.py -v
       or: python -m unittest tests.test_json_database
"""
import unittest
import asyncio
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import Database


class TestJSONDatabase(unittest.TestCase):
    """Test JSON file-based database operations"""

    def setUp(self):
        """Set up test fixtures"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Create a clean test database
        self.test_db_path = os.path.join(os.path.dirname(__file__), '..', 'test_database.json')

        # Override the database path for testing
        Database._get_db_path = classmethod(lambda cls: self.test_db_path)

        # Create clean database
        with open(self.test_db_path, 'w') as f:
            json.dump({"guilds": []}, f)

    def tearDown(self):
        """Clean up"""
        self.loop.close()

        # Remove test database
        if hasattr(self, 'test_db_path') and os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_guild_creation(self):
        """Test creating a new guild"""
        async def test():
            # Create guild
            await Database.create_database(123456, "Test Guild")
            # Check if exists
            exists = await Database.guild_in_database(123456)
            self.assertTrue(exists)

        self.loop.run_until_complete(test())

    def test_member_creation(self):
        """Test creating a member in a guild"""
        async def test():
            # Create guild
            await Database.create_database(111111, "Test Guild 2")
            # Create member
            await Database.create_member(111111, 222222, "testuser")
            # Check if exists
            member = await Database.member_in_database(111111, 222222)
            self.assertIsNotNone(member)
            self.assertEqual(member["name"], "testuser")
            self.assertEqual(member["nword_count"], 0)

        self.loop.run_until_complete(test())

    def test_increment_nword_count(self):
        """Test incrementing n-word count"""
        async def test():
            # Setup
            await Database.create_database(333333, "Test Guild 3")
            await Database.create_member(333333, 444444, "user1")

            # Increment count
            await Database.increment_nword_count(333333, 444444, 5)

            # Check count
            member = await Database.member_in_database(333333, 444444)
            self.assertEqual(member["nword_count"], 5)

            # Increment again
            await Database.increment_nword_count(333333, 444444, 3)
            member = await Database.member_in_database(333333, 444444)
            self.assertEqual(member["nword_count"], 8)

        self.loop.run_until_complete(test())

    def test_vote_system(self):
        """Test voting system"""
        async def test():
            # Setup
            await Database.create_database(555555, "Test Guild 4")
            await Database.create_member(555555, 666666, "user_to_vote")
            await Database.create_member(555555, 777777, "voter1")
            await Database.create_member(555555, 888888, "voter2")

            # Vote with threshold of 2
            await Database.cast_vote("vote", 555555, 2, 777777, 666666)
            member = await Database.member_in_database(555555, 666666)
            self.assertFalse(member["is_black"])  # Not enough votes

            # Second vote - should verify
            await Database.cast_vote("vote", 555555, 2, 888888, 666666)
            member = await Database.member_in_database(555555, 666666)
            self.assertTrue(member["is_black"])  # Enough votes now

        self.loop.run_until_complete(test())

    def test_get_nword_server_total(self):
        """Test getting total n-word count for server"""
        async def test():
            # Setup
            await Database.create_database(999999, "Test Guild 5")
            await Database.create_member(999999, 111111, "user1")
            await Database.create_member(999999, 222222, "user2")

            # Add counts
            await Database.increment_nword_count(999999, 111111, 10)
            await Database.increment_nword_count(999999, 222222, 15)

            # Check total
            total = await Database.get_nword_server_total(999999)
            self.assertEqual(total, 25)

        self.loop.run_until_complete(test())

    def test_get_global_nword_count(self):
        """Test getting global n-word count"""
        async def test():
            # Setup - create multiple guilds
            await Database.create_database(1111111, "Guild A")
            await Database.create_database(2222222, "Guild B")

            await Database.create_member(1111111, 3333333, "user1")
            await Database.create_member(2222222, 4444444, "user2")

            # Add counts
            await Database.increment_nword_count(1111111, 3333333, 20)
            await Database.increment_nword_count(2222222, 4444444, 30)

            # Check global total
            total = await Database.get_global_nword_count()
            self.assertGreaterEqual(total, 50)  # At least our counts

        self.loop.run_until_complete(test())

    def test_get_member_list(self):
        """Test getting ranked member list"""
        async def test():
            # Setup
            await Database.create_database(5555555, "Guild Ranking")
            await Database.create_member(5555555, 11111, "user1")
            await Database.create_member(5555555, 22222, "user2")
            await Database.create_member(5555555, 33333, "user3")

            # Add different counts
            await Database.increment_nword_count(5555555, 11111, 10)
            await Database.increment_nword_count(5555555, 22222, 30)
            await Database.increment_nword_count(5555555, 33333, 20)

            # Get ranking
            members = await Database.get_member_list(5555555)

            # Check order (should be descending by nword_count)
            self.assertEqual(members[0]["name"], "user2")  # 30
            self.assertEqual(members[1]["name"], "user3")  # 20
            self.assertEqual(members[2]["name"], "user1")  # 10

        self.loop.run_until_complete(test())

    def test_settings(self):
        """Test guild settings"""
        async def test():
            # Create guild
            await Database.create_database(6666666, "Guild Settings")

            # Get empty settings
            settings = await Database.get_internal_guild_settings(6666666)
            self.assertEqual(settings, [])

            # Update settings
            new_settings = [
                {"name": "test_setting", "int_name": "test", "value": True}
            ]
            await Database.update_guild_settings(6666666, new_settings)

            # Get settings
            settings = await Database.get_internal_guild_settings(6666666)
            self.assertEqual(len(settings), 1)
            self.assertEqual(settings[0]["value"], True)

        self.loop.run_until_complete(test())


if __name__ == "__main__":
    unittest.main()

