# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
import sys
import pylab as pylab
import time

start_time = time.time()

caminho = str(sys.path[0])+"\\"

#-------------------Funções-------------------
#calcula a potencia do sinal amostrado
def potenciaSinal(sinalAmostrado):
    potencia = (1./len(sinalAmostrado))*np.sum(sinalAmostrado**2.)
    return potencia

#calcula a potencia do sinal de erro de quantificação
def potenciaErroQuant(erroQuantificado):
    potenciaErro = (1./len(erroQuantificado))*np.sum(erroQuantificado**2.)
    return potenciaErro

#calcula o SNR teorico
def SNRTeorico(potencia,R,Vmax):
    valor = 6*R + 10*np.log((3*potencia)/Vmax**2)
    return valor

#calcula o SNR pratico
def SNRPratico(potenciaSinal, potenciaErro):
    valor = 10*np.log(potenciaSinal/potenciaErro)
    return valor

#retorna um numpy array com o erro do sinal
def erroQuantificacao(sinalOriginal, sinalQuantificado):
    erroSinal = sinalOriginal - sinalQuantificado
    return erroSinal

#retorna dois numpy arrays com os valores de
#decisão e com os niveis de quantificação
def createTable(R, Vmax):
    valoresDecisao = np.arange(-Vmax , Vmax+((2.*Vmax)/(2.**R)) , (2.*Vmax)/(2.**R))
    niveisQuantificacao = np.arange(-Vmax+(Vmax/(2.**R)) , Vmax , (2.*Vmax)/(2.**R))
    return valoresDecisao, niveisQuantificacao

#retorna dois numpy arrays com o sinal quantificado
#e outro com os indices dos niveis de quantificação usados
def quantificacao(sinalAmostrado, NQ, VD):
    sinalQuantificado = np.zeros(len(sinalAmostrado))
    indiceQuant = np.zeros(len(sinalAmostrado))
    maximo = np.amax(abs(sinalAmostrado))
    for a in range(len(sinalAmostrado)):
        indice =  VD > sinalAmostrado[a]
        if(sinalAmostrado[a]==maximo):
            indiceQuant[a] = len(NQ)-1
            sinalQuantificado[a] = NQ[len(NQ)-1]
        else:
            indiceTrue = np.nonzero(indice)
            aux = int(indiceTrue[0][0]-1)
            indiceQuant[a] = aux
            sinalQuantificado[a] = NQ[aux]
    return sinalQuantificado , indiceQuant.astype('int16')

#Codifica em binario o array de Indices
#retorna um numpy array com os valores em binario a 3 bit
#os valores do array de indices
def codificaSinal(IQ, R):
    sinalCodificado = np.zeros(len(IQ)*R)
    count=0
    binario = '{0:0'+str(R)+'b}'
    for i in range(len(IQ)):
        aux = binario.format(IQ[i])
        sinalCodificado[count]=int(aux[0])
        sinalCodificado[count+1]=int(aux[1])
        sinalCodificado[count+2]=int(aux[2])
        count+=3
    return sinalCodificado.astype('int16')



def recordSignal(name, freq, signal):
    wav.write(caminho+name,freq,signal.astype('int16'))

#-------------Reverse MotherFucker-------------------

def descodificaSinal(sinalCodificado, R):
    sinalDescodificado = np.zeros(len(sinalCodificado)/R)
    count = 0
    binario = ''
    for i in range(0,len(sinalCodificado),R):
        for x in range(0,R):
            binario += str(sinalCodificado[x])
        sinalDescodificado[count]=int(binario,2)
        count+=1

    return sinalDescodificado.astype('int16')

def quantificacaoInversa(sinalDescodificado,niveisQuantificacao):
    sinalQuantInv = np.zeros(len(sinalDescodificado))
    for i in range(len(sinalDescodificado)):
        sinalQuantInv[i]=niveisQuantificacao[sinalDescodificado[i]]
    return sinalQuantInv

def CORRETUDO():
    #--------------------Variaveis-----------------------
    R = 8
    Vmax = 1
    SR=np.arange(-1,1,0.0001)
    fs = 1000
    f = 3014.
    T = np.arange(0,1,1/fs)
    A = 1000

    y = A*np.cos(2*np.pi*f*T)

    #--------------Execução de funções-------------------
    VD,NQ = createTable(R,np.amax(abs(SR)))
    SQ,IQU = quantificacao(SR , NQ, VD)
    potencia = potenciaSinal(SR)
    erro = erroQuantificacao(SR,SQ)
    potenciaErro = potenciaErroQuant(erro)
    sinalCodificado = codificaSinal(IQU, R)
    sinalDescodificado = descodificaSinal(sinalCodificado,R)
    sinalQuantInv = quantificacaoInversa(sinalDescodificado,NQ)
    recordSignal('sinosoide.wav',fs,SR)
    recordSignal('sinalQuantificado.wav',fs,SQ)
    recordSignal('sinalQuantInv.wav',fs,sinalQuantInv)


    #----------------------Prints------------------------
    print ("------------------------------------------------------------------------")
    print ("Niveis de Quantificacao: \n" + str(NQ))
    print ("------------------------------------------------------------------------")
    print ("Valores de Decisao: \n" + str(VD))
    print ("------------------------------------------------------------------------")
    print ("Potencia do sinal: " + str(potencia))
    print ("------------------------------------------------------------------------")
    print ("sinalQuantificado: \n" + str(SQ))
    print ("------------------------------------------------------------------------")
    print ("Indices de Quantificacao utilizados: \n" + str(IQU))
    print ("------------------------------------------------------------------------")
    print ("Erro de Quantificacao: \n" + str(erro))
    print ("------------------------------------------------------------------------")
    print ("Potencia do Erro de Quantificacao: \n" + str(potenciaErro))
    print ("------------------------------------------------------------------------")
    print ("Codificacao: \n" + str(sinalCodificado))
    print ("------------------------------------------------------------------------")
    print ("Descodificacao: \n" + str(sinalDescodificado))
    print ("------------------------------------------------------------------------")
    print ("Quantificacao Inversa: \n" + str(sinalQuantInv))
    print ("------------------------------------------------------------------------")



    #-----------------------Plots-----------------------
    # Tsq=np.arange(0,len(SQ))
    # plt.grid(True)
    # plt.plot(Tsq,SQ, label='SinalQuantificado')
    # plt.plot(Tsq,SR, label='SinalRampa')
    # plt.legend(loc='lower right')
    # plt.show()


def EX3AQ():
    R = 3
    SR=np.arange(-1,1,0.0001)
    VD,NQ = createTable(R,np.amax(abs(SR)))
    SQ,IQU = quantificacao(SR , NQ, VD)
    Tsq=np.arange(0,len(SQ))
    plt.grid(True)
    plt.plot(Tsq,SQ, label='SinalQuantificado')
    plt.plot(Tsq,SR, label='SinalRampa')
    plt.legend(loc='lower right')
    plt.show()

def EX3BQ():
    R = 3
    SR=np.arange(-1,1,0.0001)
    VD,NQ = createTable(R,np.amax(abs(SR)))
    SQ,IQU = quantificacao(SR , NQ, VD)
    erro = erroQuantificacao(SR,SQ)
    plt.hist(erro)
    pylab.ylim([1950,2050])
    plt.show()

def EX3CQ():
    R = [3,4,5,6,7,8]
    SR=np.arange(-1,1,0.0001)
    arraySNRpratico = np.zeros(len(R))
    arraySNRteorico = np.zeros(len(R))
    for i in range(len(R)):
        VD,NQ = createTable(R[i],np.amax(abs(SR)))
        SQ,IQU = quantificacao(SR , NQ, VD)
        erro = erroQuantificacao(SR,SQ)
        potenciaErro = potenciaErroQuant(erro)
        potencia = potenciaSinal(SR)
        auxSNRP = SNRPratico(potencia,potenciaErro)
        arraySNRpratico[i] = auxSNRP
        auxSNRT = SNRTeorico(potencia,R[i],np.amax(abs(SR)))
        arraySNRteorico[i] = auxSNRT

    B = np.vstack((arraySNRteorico,arraySNRpratico))
    fig,axs =plt.subplots(1,1)
    clust_data = B
    collabel=("R=3", "R=4", "R=5", "R=6", "R=7", "R=8")
    rowlabel=("SNRTeorico","SNRPratico")
    axs.axis('off')
    the_table = axs.table(cellText=clust_data,colLabels=collabel,rowLabels=rowlabel,loc='center')
    plt.show()

def EX4AQ():
    fsRecord, data = wav.read(caminho + 'sinaldevoz8khz.wav')
    plt.hist(data)
    plt.show()

def EX4BQ():
    fsRecord, data = wav.read(caminho + 'sinaldevoz8khz.wav')
    plt.hist(data)
    plt.show()

def EX4CQ():
    R = [3,4,5,6,7,8]
    fsRecord, data = wav.read(caminho + 'sinaldevoz8khz.wav')
    arraySNRpratico = np.zeros(len(R))
    arraySNRteorico = np.zeros(len(R))
    for i in range(len(R)):
        VD,NQ = createTable(R[i],np.amax(abs(data)))
        SQ,IQU = quantificacao(data , NQ, VD)
        erro = erroQuantificacao(data,SQ)
        potenciaErro = potenciaErroQuant(erro)
        potencia = potenciaSinal(data)
        auxSNRP = SNRPratico(potencia,potenciaErro)
        arraySNRpratico[i] = auxSNRP
        auxSNRT = SNRTeorico(potencia,R[i],np.amax(abs(data)))
        arraySNRteorico[i] = auxSNRT

    B = np.vstack((arraySNRteorico,arraySNRpratico))
    fig,axs =plt.subplots(2,1)
    clust_data = B
    collabel=("R=3", "R=4", "R=5", "R=6", "R=7", "R=8")
    rowlabel=("SNRTeorico","SNRPratico")
    axs[0].axis('off')
    the_table = axs[0].table(cellText=clust_data,colLabels=collabel,rowLabels=rowlabel,loc='center')

    axs[1].plot(R,arraySNRteorico,'o',label='SNRteorico')
    axs[1].plot(R,arraySNRpratico,'o',label='SNRpratico')
    axs[1].legend(loc='upper left')
    plt.show()

if __name__=="__main__":
    # EX3AQ()
    # EX3BQ()
    # EX3CQ()
    # EX4AQ()
    # EX4BQ()
    # EX4CQ()


print("--- %s seconds ---" % (time.time() - start_time))
