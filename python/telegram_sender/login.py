import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession

from config import API_ID, API_HASH, PHONE, PASSWORD, PROXY


async def main():
    print("=" * 50)
    print("Telegram Userbot 登录工具")
    print("=" * 50)

    client = TelegramClient(
        StringSession(),
        API_ID,
        API_HASH,
        proxy=PROXY
    )

    await client.connect()

    if await client.is_user_authorized():
        print("已经登录！")
        session_string = client.session.save()
        print(f"\n你的 Session String:\n{session_string}\n")
        print("请保存上面的 Session String 到 config.py 中")
    else:
        print(f"正在向 {PHONE} 发送验证码...")

        try:
            sent_code = await client.send_code_request(PHONE)
            print("验证码已发送！")
            print("- 检查 Telegram App 内通知")
            print("- 检查短信")
            print("- 等待语音电话")

            code = input("\n请输入验证码: ").strip()

            try:
                await client.sign_in(PHONE, code, phone_code_hash=sent_code.phone_code_hash)
                print("\n登录成功！")

                session_string = client.session.save()
                print(f"\n你的 Session String:\n{session_string}\n")
                print("请保存上面的 Session String 到 config.py 中")

            except SessionPasswordNeededError:
                print("\n该账号开启了两步验证")
                pwd = input("请输入两步验证密码: ").strip()
                await client.sign_in(password=pwd)

                session_string = client.session.save()
                print(f"\n登录成功！\nSession String:\n{session_string}\n")

        except Exception as e:
            print(f"登录失败: {e}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
