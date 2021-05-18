from PIL import Image
# from answers import POSITIVE, NEGATIVE
import pytesseract
import json, sys
import base64
import pathlib
import string
PATH = "C:/Users/Joao/Documents/Projetos/TCC/fake-news-detector/src/"
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# POSITIVE = ["sim", "s", "certo", "correto", "isso", "isso mesmo", "ok"]
# NEGATIVE = ["não", "n", "errado", "incorreto", "não é isso", "está errado", "ok"]

file = open(PATH + "tokens/base64.json")
data = json.load(file)
data['img'] = data['img'].replace("data:image/jpeg;base64,", "")
img = base64.b64decode(data['img'])
filename = PATH + "assets/img/received/img.jpg"
with open(filename, 'wb') as f:
    f.write(img)
print( pytesseract.image_to_string(Image.open(filename), lang='por'))




# print("O texto está correto?")
# res = input()

# if res in POSITIVE:
#     print("Estou analisando a notícia, aguarde um momento...")
# elif res in NEGATIVE:
#     print("Por favor, me informe o texto correto.")
# else: 
#     print("Não entendi, repete por favor.")

# from newsfetch.news import newspaper
# news = newspaper('https://g1.globo.com/jornal-nacional/noticia/2021/04/05/numero-de-brasileiros-que-vivem-na-pobreza-quase-triplicou-em-seis-meses-diz-fgv.ghtml')
# news = newspaper('https://www.sensacionalista.com.br/2020/10/21/homem-que-ainda-estava-de-quarentena-e-declarado-morto-pela-familia-e-amigos/')
# news = newspaper('https://g1.globo.com/mundo/noticia/2021/05/11/noite-de-bombardeios-israelenses-e-lancamento-de-foguetes-termina-com-ao-menos-22-mortos-em-gaza.ghtml')
# https://www.sensacionalista.com.br/2020/09/22/bolsonaro-diz-na-onu-que-se-houver-queimadas-no-brasil-ele-quer-que-r-89-mil-caiam-na-conta-de-sua-mulher/
# https://noticias.uol.com.br/colunas/diogo-schelp/2021/05/11/em-cpi-presidente-da-anvisa-vai-contra-falas-de-bolsonaro-sobre-vacinas.htm
# news = newspaper('https://www.odebateon.com.br/vergonhoso-roberto-castelo-branco-se-auto-concedeu-bonus-milionario-na-petrobras/')
# print(news.article)
# text = news.article
# text = 'Coveiro com traje de protecao contra Covid-19 antes de sepultamento noturno no Cemiterio da Vila Formosa, em Sao Paulo, nesta quinta-feira (25) -- Foto: Amanda Perobelli/Reuters 1 de 1 Coveiro com traje de protecao contra Covid-19 antes de sepultamento noturno no Cemiterio da Vila Formosa, em Sao Paulo, nesta quinta-feira (25) -- Foto: Amanda Perobelli/Reuters Com 660 mortes por Covid-19 registradas neste sabado (8), o estado de Sao Paulo chegou a 100.649 vidas perdidas para a doenca desde o inicio da pandemia, segundo dados divulgados pela Fundacao Sistema Estadual de Analise de Dados (Seade). O numero foi alcancado pouco mais de um ano apos a confirmacao da primeira morte, em 12 de marco de 2020. Atingida na primeira semana de maio, a marca reflete a dramatica estatistica registrada em abril, considerado o mes mais letal de toda a pandemia no estado e no pais, superando o recorde anterior, de marco de 2021. Se fosse um pais, o estado de Sao Paulo seria o nono com mais vitimas, mais do que o total de obitos de paises mais populosos, como Alemanha, Espanha e Colombia. Em 29 de abril, o Brasil ultrapassou 400 mil mortes por Covid-19. A marca dos primeiros 100 mil obitos no Brasil foi atingida quase 5 meses - 149 dias - apos a primeira pessoa morrer pela doenca no pais. Dos 100 mil para os 200 mil, passaram-se outros 5 meses - 152 dias. Mas para chegar aos 300 mil, foram necessarios somente 76 dias, numero que agora caiu quase pela metade. Entre marco e abril, foram 100 mil mortes registradas em apenas 36 dias. Ou seja, UMA EM CADA QUATRO PESSOAS que morreram pela doenca no Brasil perdeu a vida nos ultimos TRINTA E SEIS DIAS. Uma das vitimas e o comerciante Joao Parreira, de 48 anos, que nao deixou um vazio apenas na familia formada por cinco filhos e a esposa, mas em toda a comunidade do Jardim Peri, na Zona Norte de Sao Paulo, onde ele liderava um projeto social que atendia a mais de 120 criancas carentes. Um dos jovens ajudados pela ONG, que virou cantor e tem conquistado fas em SP, criou uma musica que resume o sentimento da comunidade sobre o trabalho do comerciante, que marcou para sempre a trajetoria de vida de muitos do Jardim Peri. "Voce \'ta fazendo falta. Esperava voce ter alta. \'Ta dificil acreditar que voce nao vai voltar. Voce foi guerreiro, te desejo um bom lugar. Eu olho para o ceu ao anoitecer, a estrela que mais brilha e voce. Olha como doi, perder um grande heroi. Saudade machuca e corroi", diz a letra da musica do Nego Helio. Morte de lider comunitario por Covid deixa 120 criancas \'orfas\' em projeto em SP Internacoes e casos em SP Sao 21.565 pacientes internados no estado, sendo 10.047 em unidades de terapia intensiva e 11.518 em enfermaria. A taxa de ocupacao dos leitos de UTI no estado e de 78,5% e na Grande Sao Paulo e de 76,5%. O estado de Sao Paulo chegou a 2.997.282 casos confirmados da doenca desde o comeco da pandemia. Nas ultimas 24 horas, foram confirmadas 1.243 novas mortes e 27.602 novos casos. No dia seis de abril, o estado registrou o recorde de mortes por Covid-19 ao contabilizar 1.389 obitos em um dia (veja mais no video abaixo). VIDEO: SP bate novo recorde e registra 1.389 mortes por Covid-19 em 24 horas Internacoes param de cair No estado de Sao Paulo, o numero diario de novas internacoes pela doenca, que estava em queda, parou de cair ha pouco mais de uma semana. A media movel de internacoes chegou ao seu maior nivel em 26 de marco, com 3.399 hospitalizacoes ao dia. Desde entao, o indice passou a cair seguidamente mas, desde o final de abril, o indicador esta estavel. Na terca (4), a media foi de 2.222 internacoes diarias. O numero e apenas 5% menor do que o verificado 14 dias atras, o que indica tendencia de estabilidade. Na ultima semana, a queda ficou ainda mais discreta: o indice desta terca foi praticamente identico ao verificado 7 dias atras, em 27 de abril, quando a media era de 2.223 internacoes ao dia. Apos um mes de queda, a media diaria de novas internacoes por Covid-19 chegou a subir por alguns dias no final de abril. Segundo especialistas, ainda e cedo para avaliar se a curva voltara a subir de forma constante ou entrara em estabilidade, mas eles alertam que a desaceleracao da queda e um ponto de atencao. "Os dados dos ultimos dois dias comecam a indicar essa estabilizacao. Talvez sugira uma tendencia ate de piora. Entao, na melhor das hipoteses, a gente deixou de melhorar. A gente estabilizou, mas estabilizou num patamar muito alto", afirma o epidemiologista Marcio Bittencourt. A chegada do inverno tambem preocupa porque a pressao nos hospitais costuma aumentar por conta de outras doencas respiratorias, AVCs e infartos. "Se a gente entrar neste periodo [inverno] com a taxa atual, mesmo que estavel, mesmo que sem nenhuma piora, ja e uma situacao bastante preocupante", diz Bittencourt. Flexibilizacao da quarentena Apesar dos recordes de abril, o governo de Sao Paulo se diz otimista com os indicadores da Covid-19, considerando especialmente a ocupacao de Unidades de Terapia Intensiva (UTI) e o total de pacientes internados. As restricoes da quarentena estadual comecaram a ser flexibilizadas no dia 12 de abril, quando acabou a fase emergencial, a mais rigida, e foi retomada a fase vermelha. Desde entao, a fase vermelha tambem foi encerrada e o governo anunciou uma nova etapa da quarentena, a chamada "fase de transicao", em vigor desde o dia 18 do mes passado. Abril ja o mes mais letal da pandemia: 15.975 pessoas morreram no estado'
# text = text.lower()
# text = text.replace('-', ' ').replace(':', '').replace('/', '').replace('\\', '').replace('(', '').replace(')', '').replace(',', '').replace('.', '').replace('%', '').replace('"', '').replace('\'', '').replace('\n', ' ').replace('https?://\S+|www\.\S+', '').replace('\\W', ' ').replace('\n', '').replace(' +', ' ').replace('^ ', '').replace(' $', '').replace(';', '').replace('?', '')
# REMOVER PONTUAÇÕES::
# first_text = re.sub('\[[^]]*\]', ' ', first_text)
# first_text = re.sub('[^a-zA-Z]',' ',first_text)  # replaces non-alphabets with spaces

    # nopunc = [char for char in s if char not in string.punctuation]
# print(text)
# chatbot = ChatBot(
#     'Genuíno',
#     logic_adapters=[
#         "chatterbot.logic.BestMatch",
#         "chatterbot.logic.TimeLogicAdapter"
#     ],
#     storage_adapter='chatterbot.storage.SQLStorageAdapter',
#     database_uri='sqlite:///db.sqlite3'
# )
# trainer = ChatterBotCorpusTrainer(chatbot)

# trainer.train('chatterbot.corpus.portuguese.genuino')
# bot_input = chatbot.get_response('Genuíno')
# print(bot_input)