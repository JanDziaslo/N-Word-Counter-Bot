"""JSON file-based database utility class with database commands"""
import os
import logging
import json
import asyncio

# Database file path
DB_FILE = "bot_database.json"

# Default database structure
DEFAULT_DB = {"guilds": []}


class Database:
    """JSON file-based database"""
    _lock = asyncio.Lock()

    @classmethod
    def _get_db_path(cls) -> str:
        """Get absolute path to database file"""
        return os.path.join(os.path.dirname(__file__), "..", DB_FILE)

    @classmethod
    def _load_database(cls) -> dict:
        """Load database from JSON file"""
        db_path = cls._get_db_path()
        try:
            if os.path.exists(db_path):
                with open(db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return DEFAULT_DB.copy()
        except json.JSONDecodeError:
            logging.error(f"Failed to decode {db_path}, using default database")
            return DEFAULT_DB.copy()

    @classmethod
    def _save_database(cls, data: dict) -> None:
        """Save database to JSON file"""
        db_path = cls._get_db_path()
        try:
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Failed to save database: {e}")

    @classmethod
    async def _async_load_database(cls) -> dict:
        """Async load database"""
        async with cls._lock:
            return cls._load_database()

    @classmethod
    async def _async_save_database(cls, data: dict) -> None:
        """Async save database"""
        async with cls._lock:
            cls._save_database(data)

    def __init__(self):
        """Initialize database connection"""
        logging.info("Initialized JSON file-based database")
        print("Initialized JSON file-based database")

    @classmethod
    async def guild_in_database(cls, guild_id: int) -> bool:
        """Return True if guild is already recorded in database"""
        db = await cls._async_load_database()
        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                return True
        return False

    @classmethod
    async def create_database(cls, guild_id: int, guild_name: str) -> None:
        """Initialize guild template in database"""
        db = await cls._async_load_database()

        # Check if guild already exists
        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                return

        new_guild = {
            "guild_id": guild_id,
            "guild_name": guild_name,
            "members": [],
            "settings": []
        }

        db.setdefault("guilds", []).append(new_guild)
        await cls._async_save_database(db)
        logging.info(f"Guild added! {guild_name} with id {guild_id}")

    @classmethod
    async def update_guilds(cls):
        """Update all guilds in database to have a settings field if they don't already."""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if "settings" not in guild:
                guild["settings"] = []

        await cls._async_save_database(db)

    @classmethod
    async def get_internal_guild_settings(cls, guild_id: int) -> list:
        """Return guild settings as a list"""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                return guild.get("settings", [])

        return []

    @classmethod
    async def update_guild_settings(cls, guild_id: int, settings: list) -> None:
        """Update guild settings"""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                guild["settings"] = settings
                await cls._async_save_database(db)
                return

    @classmethod
    async def get_guild_settings(cls, guild_id: int):
        new_settings = {}
        settings = await cls.get_internal_guild_settings(guild_id)
        for setting in settings:
            new_settings[setting["int_name"]] = setting
        return new_settings

    @classmethod
    async def member_in_database(
            cls, guild_id: int, member_id: int) -> dict | None:
        """Return member dict if member is already recorded in guild database"""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                for member in guild.get("members", []):
                    if member["id"] == member_id:
                        return member

        return None

    @classmethod
    async def create_member(cls, guild_id: int, member_id: int, member_name: str) -> None:
        """Initialize member data in guild database"""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                new_member = {
                    "id": member_id,
                    "name": member_name,
                    "nword_count": 0,
                    "is_black": False,
                    "has_pass": False,
                    "passes": 0,
                    "voters": []
                }
                guild.setdefault("members", []).append(new_member)
                await cls._async_save_database(db)
                return

    @classmethod
    async def increment_nword_count(cls, guild_id: int, member_id: int, count: int) -> None:
        """Add to n-word count of person's data info in server"""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                for member in guild.get("members", []):
                    if member["id"] == member_id:
                        member["nword_count"] += count
                        await cls._async_save_database(db)
                        return

    @classmethod
    async def increment_passes(cls, guild_id: int, member_id: int, count: int) -> None:
        """Add to user's total available n-word passes in server"""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                for member in guild.get("members", []):
                    if member["id"] == member_id:
                        member["passes"] += count
                        await cls._async_save_database(db)
                        return

    @classmethod
    async def get_total_documents(cls) -> int:
        """Return total number of guilds in database"""
        db = await cls._async_load_database()
        return len(db.get("guilds", []))

    @classmethod
    async def get_nword_server_total(cls, guild_id: int) -> int:
        """Return integer sum of total n-words said in a server"""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                total = 0
                for member in guild.get("members", []):
                    total += member.get("nword_count", 0)
                return total

        return 0

    @classmethod
    async def get_all_time_servers(cls, limit: int) -> list:
        """Return the servers with the highest recorded n-word count out of all servers"""
        db = await cls._async_load_database()

        servers = []
        for guild in db.get("guilds", []):
            total = 0
            for member in guild.get("members", []):
                total += member.get("nword_count", 0)

            servers.append({
                "_id": {
                    "guild_id": guild["guild_id"],
                    "guild_name": guild["guild_name"]
                },
                "nword_count": total
            })

        # Sort by nword_count descending and limit
        servers.sort(key=lambda x: x["nword_count"], reverse=True)
        return servers[:limit]

    @classmethod
    async def get_all_time_counts(cls, limit: int) -> list:
        """Return the members with the highest recorded n-word count out of all servers"""
        db = await cls._async_load_database()

        all_members = []
        for guild in db.get("guilds", []):
            for member in guild.get("members", []):
                all_members.append({
                    "member": member["name"],
                    "nword_count": member.get("nword_count", 0)
                })

        # Sort by nword_count descending and limit
        all_members.sort(key=lambda x: x["nword_count"], reverse=True)
        return all_members[:limit]

    @classmethod
    async def get_member_list(cls, guild_id: int) -> list:
        """Return sorted ranked list of member objects based on n-word frequency"""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                members = guild.get("members", [])
                # Sort by nword_count descending
                sorted_members = sorted(
                    members,
                    key=lambda x: x.get("nword_count", 0),
                    reverse=True
                )

                # Return formatted list
                return [
                    {
                        "name": member["name"],
                        "is_black": member.get("is_black", False),
                        "has_pass": member.get("has_pass", False),
                        "nword_count": member.get("nword_count", 0)
                    }
                    for member in sorted_members
                ]

        return []

    @classmethod
    async def cast_vote(
        cls, type: str, guild_id: int, vote_threshold: int,
        voter_id: int, votee_id: int
    ) -> dict | None:
        """Insert voter id into votee's voter list in database"""
        db = await cls._async_load_database()

        for guild in db.get("guilds", []):
            if guild["guild_id"] == guild_id:
                for member in guild.get("members", []):
                    if member["id"] == votee_id:
                        if type == "vote":
                            if voter_id not in member.get("voters", []):
                                member.setdefault("voters", []).append(voter_id)
                        else:  # unvote
                            if voter_id in member.get("voters", []):
                                member["voters"].remove(voter_id)

                        # Check if enough votes
                        if len(member.get("voters", [])) >= vote_threshold:
                            member["is_black"] = True
                        else:
                            member["is_black"] = False

                        await cls._async_save_database(db)
                        return member

        return None

    @classmethod
    async def get_global_nword_count(cls) -> int:
        """Return integer sum of total n-words said in all servers"""
        db = await cls._async_load_database()

        total = 0
        for guild in db.get("guilds", []):
            for member in guild.get("members", []):
                total += member.get("nword_count", 0)

        return total
