# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from bot.models.server import Server
from bot.db.database import Database


class Servers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__servers = {}
        self.__players = {}

    @commands.Cog.listener()
    async def on_ready(self):
        # add all guilds bot is on to list of servers
        self.__add_active_servers()
        self.__add_db_players()

    def __add_active_servers(self):
        activeservers = self.bot.guilds

        for guild in activeservers:
            s = Server()
            self.add_server(guild, s)

    def __add_db_players(self):
        db = Database("db/database.db")
        sql = 'SELECT * FROM player'
        for row in db.cursor.execute(sql):
            self.__players[row[0]] = row[1]

    def add_server(self, guild: discord.Guild, server: Server):
        self.__servers[guild] = server

    def get_server(self, guild: discord.Guild):
        return self.__servers.get(guild)


def setup(bot):
    bot.add_cog(Servers(bot))