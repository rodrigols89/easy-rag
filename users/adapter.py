from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class NoMessageAccountAdapter(DefaultAccountAdapter):
    """
    Adapter para suprimir mensagens que o allauth adicionaria ao sistema
    de messages.

    Aqui fazemos nada no add_message — assim o allauth não adiciona
    mensagens.
    """
    def add_message(self, request, level, message_template,
                    message_context=None):
        # Return sem chamar super()
        # Evita que o allauth chame messages.add_message(...)
        return


class NoMessageSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Mesmo para socialaccount, caso mensagens venham de lá."""
    def add_message(self, request, level, message_template,
                    message_context=None):
        # Return sem chamar super()
        # Evita que o allauth chame messages.add_message(...)
        return
