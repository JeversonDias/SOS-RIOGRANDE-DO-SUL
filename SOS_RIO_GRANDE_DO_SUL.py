import tkinter as tk 
import webbrowser 
import pandas as pd 
import numpy as np 
import google.generativeai as genai 

# Configurando a API key 
GPPGLE_API_KEY = "Sua_Chave_Aqui" 
genai.configure(api_key=GPPGLE_API_KEY) 

# URL do vídeo do YouTube para as aulas 
#url_video_aulas = "https://www.vakinha.com.br/vaquinha/a-maior-campanha-solidaria-do-rs" 

# Criando a janela principal 
root = tk.Tk() 
root.title("myGeminy") 

# Definindo a cor de fundo da janela como a da bandeira do Rio Grande do Sul 
cor_bandeira_rs = "#191970"  # Cor azul 
root.configure(bg=cor_bandeira_rs) 

# Determinando a largura e altura da janela 
largura_janela = root.winfo_screenwidth() 
altura_janela = root.winfo_screenheight() 
root.geometry(f"{int(largura_janela * 0.4)}x{int(altura_janela * 0.6)}") 

# Configurando para abrir em tela cheia 
root.attributes("-fullscreen", True) 

# Diminuindo o tamanho da fonte e configurando em negrito 
fonte = ("Helvetica", int(14 - 1), "bold")  #######################################################
# Função para limpar a barra de pesquisa 
def limpar_pesquisa(): 
    entry.delete(0, tk.END) 

# Função para limpar a caixa de texto 
def limpar_caixa_texto(): 
    text_box.delete(1.0, tk.END) 

# Função para lidar com a geração de texto e exibição de resultados 
def search(): 
    query = entry.get() 
    if query: 
        limpar_caixa_texto() 
        trecho = gerar_e_buscar_consulta(query, df, model) 
        response = gerar_resposta_interativa(trecho) 
        text_box.insert(tk.END, response + "\n\n") 
    else: 
        messagebox.showinfo("Aviso", "Por favor, digite uma consulta.") 

# Função para gerar respostas interativas mais descontraídas 
def gerar_resposta_interativa(texto): 
    generation_config = { 
        "temperature": 0  # Ajuste de temperatura para tornar as respostas mais descontraídas 
    } 
    prompt = f"Reescreva este texto de uma forma mais descontraída, sem adicionar informações que não façam parte do texto: {texto}" 
    model_2 = genai.GenerativeModel("gemini-1.0-pro", generation_config=generation_config) 
    response = model_2.generate_content(prompt) 
    return response.text 

# Função para integrar o código de geração de texto com a base de dados 
def gerar_e_buscar_consulta(consulta, base, model): 
    embedding_da_consulta = genai.embed_content(model=model, content=consulta, task_type="RETRIEVAL_QUERY")["embedding"] 
    produtos_escalares = np.dot(np.stack(df["Embeddings"]), embedding_da_consulta) 
    indice = np.argmax(produtos_escalares) 
    return df.iloc[indice]["Conteudo"] 

# Criando e posicionando os elementos na janela 
label = tk.Label(root, text="Digite sua consulta:", font=fonte, bg=cor_bandeira_rs, fg="white") 
label.pack(pady=10) 

entry = tk.Entry(root, width=int(largura_janela * 0.7), font=fonte) 
entry.pack(pady=5) 

button = tk.Button(root, text="Buscar", command=search, font=fonte) 
button.pack(pady=10) 



# Criando a caixa de texto com a nova fonte
text_box = tk.Text(root, width=int(largura_janela * 0.7), height=15, font=("Helvetica", 16, "bold"), bg="yellow", fg="red" )
text_box.pack(pady=20) ###################################################################################################################################

# Adicionando texto grande "SOS RIO GRANDE DO SUL" no centro da janela em vermelho 
sos_label = tk.Label(root, text="SOS RIO GRANDE DO SUL\n\n\n", font=("Helvetica", 48, "bold"), bg=cor_bandeira_rs, fg="#FF0000") 
sos_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER) 

sos_label2 = tk.Label(root, text="AJUDE-NOS A SALVAR VIDAS\n", font=("Helvetica", 42, "bold"), bg=cor_bandeira_rs, fg="#00FFB7") 
sos_label2.place(relx=0.5, rely=0.8, anchor=tk.CENTER) # Ajustei a posição vertical para evitar sobreposição

sos_label3 = tk.Label(root, text="VAMOS ENTRE LÁGRIMAS DE ESPERANÇA   🙏 SÓ VAMOS 😢", font=("Helvetica", 40, "bold"), bg=cor_bandeira_rs, fg="#F8F000") 
sos_label3.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
# Frame para os botões de ajuda 
frame_botao_ajuda = tk.Frame(root, bg=cor_bandeira_rs) 
frame_botao_ajuda.pack(side=tk.BOTTOM, pady=(50, 0))  # Adicionando 50 pixels de margem superior e 0 pixels de margem inferior 

# Links de ajuda 
links_ajuda = [ 
    ("https://www.vakinha.com.br/vaquinha/a-maior-campanha-solidaria-do-rs", "Vaquinha online Apoio as vidas!"), 
    ("https://www.metropoles.com/brasil/saiba-como-ajudar-o-rio-grande-do-sul", "Site Noticias Gerais Apoio as vidas!"), 
    ("https://www.uol.com.br/ecoa/ultimas-noticias/2024/05/08/como-ser-voluntario-voluntariado-rs-rio-grande-do-sul.htm?cmpid=copiaecola", "Seja Voluntário Apoio as vidas!"), 
    ("https://linktr.ee/gradbrasil", "Ajuda aos animais Apoio as vidas!"), 
    ("https://www.youtube.com/watch?v=HKYqZ9MdWbo", "Live Podelas  S.O.S (EVENTO SÉRIO)"), 
] 

# Função para lidar com o clique nos botões de ajuda 
def abrir_link(url): 
    webbrowser.open(url) 

# Adicionando botões para ajuda 
for url, descricao in links_ajuda: 
    ajuda_button = tk.Button(frame_botao_ajuda, text=descricao, command=lambda u=url: abrir_link(u), font=fonte) 
    ajuda_button.pack(side=tk.LEFT, padx=10) 

# Carregando os dados e integrando com o modelo de geração de texto
DOCUMENT1 = {
    "Titulo": "A cronologia da tragédia no Rio Grande do Sul",
    "Conteudo" : "Em pouco mais de uma semana, mais de 400 municípios gaúchos tiveram bairros inteiros engolidos por uma chuva que não parava de cair."
}

DOCUMENT2 = {
    "Titulo": "Chuvas intensas no fim de semana podem agravar situação no Rio Grande do Sul",
    "Conteudo" : "A previsão de um grande volume de chuvas entre sexta-feira (10/5) e segunda (13/5) em todo o Rio Grande do Sul, segundo os serviços meteorológicos, pode agravar a situação dramática que já vive o Estado por causas das enchentes que já duram duas semanas."
}

DOCUMENT3 = {
    "Titulo" : "O gaúcho de 59 anos que resgatou 300 pessoas de caiaque – sem saber nadar: 'Não posso me deprimir diante da tragédia'",
    "Conteudo" : "Em seus 59 anos de vida, o gaúcho Ivan Brizola nunca aprendeu a nadar. Mas quando fortes enchentes atingiram o Rio Grande do Sul neste mês, ele pediu emprestado um caiaque - que também nunca tinha usado - e saiu resgatando pessoas em meio à inundação.."
}


DOCUMENT4 = {
    "Titulo" : "Moradores às escuras improvisam 'patrulha' em Porto Alegre: ",
    "Conteudo" : "A enchente que inundou bairros inteiros e provocou pane na iluminação pública e nos sistemas eletrônicos de vigilância levou moradores e voluntários de equipes de socorro a improvisarem esquemas alternativos de segurança em Porto Alegre (RS)."
}

DOCUMENT5 = {
    "Titulo" : "Situação em Rio grande do Sul é terrivel",
    "Conteudo" : "A escuridão à noite e a desocupação de imóveis fizeram de algumas regiões alvos preferenciais de bandidos. Episódios de saques a lojas e ataques a voluntários em bairros de Porto Alegre e Canoas foram confirmados por vítimas e autoridades"
}

DOCUMENT6 = {
    "Titulo" : "Além do sofrimento com o aumento da água gaúchos estão tendo que conviver com aumento da criminalidade por conta dos fatos",
    "Conteudo" : "A multiplicação de relatos de crimes acompanhou o avanço da água, que atingiu em primeiro lugar o Delta do Jacuí. A região, na qual o rio homônimo deságua no Lago Guaíba, é composta por 27 ilhas entremeadas de canais, banhados e várzeas. Desse total, 16 compõem o bairro Arquipélago, de Porto Alegre."
}

DOCUMENT7 = {
    "Titulo" : "Desigualdade dói",
    "Conteudo" : "De um lado, há luxuosas residências à beira do lago, com marinas nas quais reluzem barcos esportivos e jet-skis. De outro, comunidades de catadores de lixo, autônomos e assalariados de baixa qualificação. Palco frequente de inundações, a região costuma registrar mais crimes quando a água avança."
}

DOCUMENT8 = {
    "Titulo" : "Números",
    "Conteudo" : "A maior tragédia climática da história do Rio Grande do Sul já deixou pelo menos 136 mortos e afetou mais de 2 milhões de pessoas."
}

DOCUMENT9 = {
    "Titulo" : "moradores de Porto Alegre lotam abrigo enquanto chuva volta a cair no Rio Grande do Sul",
    "Conteudo" : "A crise das enchentes em Porto Alegre entrou no sexto dia nesta quarta-feira (08/05) com boa parte da cidade na escuridão, sem água e até algumas áreas secas sendo afetadas."
}

DOCUMENT10 = {
    "Titulo" : "Resgates",
    "Conteudo" : "Também voltou a chover na capital gaúcha, o que fez a prefeitura interromper operações de resgate de pessoas ilhadas."
}

DOCUMENT11 = {
    "Titulo" : "Muita gente mobilizado-se",
    "Conteudo" : "O local, por onde já passaram cerca de 110 desalojados, segundo o pastor que coordena o projeto, oferece quatro refeições e banho quente, além de assistência médica e psicológica."
}

DOCUMENT12 = {
    "Titulo" : "Como ser voluntário no RS? Instituições e governo aceitam inscrições; veja… - Veja mais em https://www.uol.com.br/ecoa/ultimas-noticias/2024/05/08/como-ser-voluntario-voluntariado-rs-rio-grande-do-sul.htm?cmpid=copiaecola",
    "Conteudo" : "O governo do estado tem um formulário próprio para a inscrição de voluntários para o programa SOS Rio Grande do Sul. A Coordenadoria Estadual de Proteção e a Defesa Civil são responsáveis pela coleta dos dados de pessoas que desejam trabalhar no apoio aos atingidos pelas enchentes… - Veja mais em https://www.uol.com.br/ecoa/ultimas-noticias/2024/05/08/como-ser-voluntario-voluntariado-rs-rio-grande-do-sul.htm?cmpid=copiaecola"
}

DOCUMENT13 = {
    "Titulo" : "Link para ser voluntário, Para agir trabalhando em prol da reconstrução do estado Link",
    "Conteudo" : " Este é o link para a vaquinha online https://www.vakinha.com.br/vaquinha/a-maior-campanha-solidaria-do-rs"
}

DOCUMENT14 = {
    "Titulo" : "PIX AJUDA ao Rio Grande",
    "Conteudo" : "PIX do SOS Rio Grande do Sul CNPJ: 92.958.800/0001-38 (Banrisul)"
}


DOCUMENT15 = {
    "Titulo" : "Site oficial do Rio Grande do Sul",
    "Conteudo" : "Este é o link oficial para quem quiser ajudar a reconstruir Porto Alegre   https://sosenchentes.rs.gov.br/inicial"
}

DOCUMENT16 = {
    "Titulo" : "Quer ajudar os animaizinhoas envolvido na tragédia ? ",
    "Conteudo" : "Link para arrecadar fundos para a ajuda ao resgate e tratamento de animaizinhos  é https://linktr.ee/gradbrasil"
}

DOCUMENT17 = {
    "Titulo" : "Notícias Gerais sobre o Rio Grande do Sul , como ajudar, numeros etc",
    "Conteudo" : "Este é o link onde têm todos ou quase todos os meios de como ajudar o Rio Grande do Sula nesta impreitade de sobrevivência  https://www.metropoles.com/brasil/saiba-como-ajudar-o-rio-grande-do-sul"
}


DOCUMENT18 = {
    "Titulo" : "ao clicar nos botões a baixo terá link direto para poder contribuir | RS | ajudar | Olá O que são os botões",
    "Conteudo" : "Nos botões a baixo estão boa parte dos links onde vai poder contribuir com a reconstrução do estado RS Porto Alugre e também ajudar a salvar vidas agora neste primeiro momento!"
}



documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3,DOCUMENT4, DOCUMENT5, DOCUMENT6,DOCUMENT7, DOCUMENT8, DOCUMENT9,DOCUMENT10, DOCUMENT11, DOCUMENT12,DOCUMENT13,DOCUMENT14,DOCUMENT15,DOCUMENT16,DOCUMENT17,DOCUMENT18] 
df = pd.DataFrame(documents) 
model = "models/embedding-001" 

def embed_fn(title, text): 
    return genai.embed_content(model=model, content=text, title=title, task_type="RETRIEVAL_DOCUMENT")["embedding"] 

df["Embeddings"] = df.apply(lambda row: embed_fn(row["Titulo"], row["Conteudo"]), axis=1) 

# Executando o loop principal da aplicação 
root.mainloop()