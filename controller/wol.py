from wakeonlan import send_magic_packet
from controller.database import Database

class WakeOnLan:
    def __init__(self):
        self.db = Database

    @staticmethod
    def wake(mac_address: str):
        """Envoie un paquet WoL pour réveiller un ordinateur."""
        try:
            send_magic_packet(mac_address)
            print(f"Paquet WoL envoyé à {mac_address}")
        except Exception as e:
            print(f"Erreur lors de l'envoi du paquet WoL : {e}")