"""
Core module per Custom GPT Actions
Contiene client condivisi per OpenAI e Claude
"""

from .api_client import OpenAIClient, ClaudeClient, quick_openai_chat, quick_claude_chat

__all__ = ['OpenAIClient', 'ClaudeClient', 'quick_openai_chat', 'quick_claude_chat']
