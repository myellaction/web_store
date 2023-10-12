import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_API = str(os.getenv('TOKEN_API'))


__all__ = ['TOKEN_API']