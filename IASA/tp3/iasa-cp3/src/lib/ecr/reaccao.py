from ecr.comportamento import Comportamento

class Reaccao(Comportamento):

    def activar(self, percepcao):
        estimulo = self._detetar_estimulo(percepcao)
        if estimulo is not None and estimulo is not False:
            resposta = self._gerar_resposta(estimulo)
            return resposta

    def _gerar_resposta(self, estimulo):
        raise NotImplementedError

    def _detetar_estimulo(self, percepcao):
        raise NotImplementedError