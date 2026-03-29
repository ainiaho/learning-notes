import asyncio
from typing import Dict, Any, List, Union
from telethon import TelegramClient
from telethon.sessions import StringSession

from config import API_ID, API_HASH, PROXY


class TelegramBotSender:
    _instance = None

    def __new__(cls, session_string: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session_string = session_string
            cls._instance._client = None
            cls._instance._loop = None
        return cls._instance

    @property
    def client(self):
        if self._client is None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._client = TelegramClient(
                StringSession(self.session_string),
                API_ID,
                API_HASH,
                proxy=PROXY,
                loop=self._loop
            )
        return self._client

    async def connect(self):
        if not self.client.is_connected():
            await self.client.connect()

    async def send_message(
        self,
        target: str,
        text: str
    ) -> Dict[str, Any]:
        """向单个机器人/用户发送消息"""
        await self.connect()

        try:
            entity = await self.client.get_entity(target)
            message = await self.client.send_message(entity, text)

            return {
                "success": True,
                "message_id": message.id,
                "target": target,
                "text": text,
                "timestamp": str(message.date)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "target": target,
                "text": text
            }

    async def send_batch(
        self,
        messages: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """批量发送消息到多个目标

        Args:
            messages: [{"target": "@bot1", "text": "hello"}, {"target": "@bot2", "text": "hi"}]

        Returns:
            每条消息的发送结果列表
        """
        await self.connect()
        results = []

        for msg in messages:
            result = await self.send_message(msg["target"], msg["text"])
            results.append(result)

        return results

    async def get_bot_response(
        self,
        target: str,
        text: str,
        timeout: float = 10.0
    ) -> Dict[str, Any]:
        """发送消息并等待回复"""
        await self.connect()

        try:
            entity = await self.client.get_entity(target)
            sent_msg = await self.client.send_message(entity, text)

            response = None
            async for message in self.client.iter_messages(
                entity,
                limit=10,
                min_id=sent_msg.id
            ):
                sender = message.sender
                if sender and sender.bot:
                    response = message
                    break

            if response:
                return {
                    "success": True,
                    "sent_message": text,
                    "response": response.text,
                    "response_id": response.id,
                    "target": target
                }
            else:
                return {
                    "success": True,
                    "sent_message": text,
                    "response": None,
                    "message": "未收到回复",
                    "target": target
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "target": target,
                "text": text
            }

    async def get_dialogs(self, limit: int = 20):
        """获取对话列表"""
        await self.connect()

        dialogs = []
        async for dialog in self.client.iter_dialogs(limit=limit):
            entity = dialog.entity
            dialogs.append({
                "name": dialog.name,
                "id": dialog.id,
                "username": getattr(entity, 'username', None),
                "is_bot": getattr(entity, 'bot', False),
                "unread_count": dialog.unread_count
            })

        return dialogs

    async def get_me(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        await self.connect()
        me = await self.client.get_me()
        return {
            "id": me.id,
            "first_name": me.first_name,
            "last_name": me.last_name,
            "username": me.username,
            "phone": me.phone
        }
