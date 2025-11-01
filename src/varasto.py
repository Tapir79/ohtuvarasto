class Varasto:
    def __init__(self, tilavuus, alku_saldo=0):
        self.tilavuus = self._aseta_tilavuus(tilavuus)
        self.saldo = self._aseta_saldo(self.tilavuus, alku_saldo)

    def _aseta_tilavuus(self, tilavuus):
        """Palauttaa kelvollisen tilavuuden (ei negatiivista)."""
        if tilavuus > 0.0:
            return tilavuus
        return 0.0

    def _aseta_saldo(self, tilavuus, alku_saldo):
        """Palauttaa kelvollisen saldon (ei negatiivista, ei yli tilavuuden)."""
        if alku_saldo < 0.0:
            return 0.0
        if alku_saldo <= tilavuus:
            return alku_saldo
        return tilavuus

    # huom: ominaisuus voidaan myös laskea.
    # Ei tarvita erillistä kenttää viela_tilaa tms.
    def paljonko_mahtuu(self):
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        if maara < 0:
            return
        if maara <= self.paljonko_mahtuu():
            self.saldo = self.saldo + maara
        else:
            self.saldo = self.tilavuus

    def ota_varastosta(self, maara):
        if maara < 0:
            return 0.0
        if maara > self.saldo:
            kaikki_mita_voidaan = self.saldo
            self.saldo = 0.0

            return kaikki_mita_voidaan

        self.saldo = self.saldo - maara

        return maara

    def __str__(self):
        return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"
