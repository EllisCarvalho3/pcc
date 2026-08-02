# Nuttrium

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Framework-092E20?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)

Sistema web desenvolvido em **Python** utilizando o framework **Django**, destinado ao monitoramento do consumo calórico diário de estudantes, promovendo maior consciência alimentar por meio do registro de refeições, cálculo automático de calorias e definição de metas nutricionais personalizadas.

---

# Demonstração

*A imagem abaixo apresenta uma visão geral da interface do sistema.*

<p align="center">
    <img src="imagens/demonstracao_sistema.png" alt="Tela inicial do sistema" width="900">
</p>


---

# Sobre o Projeto

O **Nuttrium** é uma plataforma web desenvolvida para auxiliar estudantes no acompanhamento da alimentação diária de forma simples, intuitiva e acessível.

O sistema permite registrar refeições consumidas ao longo do dia, calcular automaticamente o total de calorias ingeridas, comparar esse valor com uma meta calórica personalizada e fornecer feedback nutricional ao usuário.

Além disso, o projeto integra uma base de dados nutricional externa para automatizar a obtenção das informações dos alimentos, reduzindo cálculos manuais e tornando o processo de monitoramento mais eficiente.

O desenvolvimento do sistema busca integrar tecnologia, educação e saúde, incentivando hábitos alimentares mais conscientes e contribuindo para a melhoria da qualidade de vida e do desempenho acadêmico dos estudantes.

---

# Objetivos

## Objetivo Geral

Desenvolver um sistema inteligente, acessível e intuitivo para auxiliar estudantes no monitoramento da ingestão calórica diária, promovendo maior consciência alimentar.

## Objetivos Específicos

- Registrar refeições diárias dos usuários;
- Calcular automaticamente calorias e macronutrientes;
- Integrar o sistema a uma base nutricional externa;
- Definir metas calóricas personalizadas;
- Comparar o consumo diário com a meta estabelecida;
- Fornecer feedback nutricional automático;
- Armazenar o histórico alimentar do usuário.

---

# Funcionalidades

- Cadastro e autenticação de usuários;
- Perfil nutricional personalizado;
- Definição automática da meta calórica;
- Registro de refeições;
- Cálculo automático de calorias;
- Consulta automática à base nutricional;
- Histórico alimentar;
- Feedback nutricional diário;
- Interface responsiva.

---

# Tecnologias Utilizadas

- Python
- Django
- SQLite
- HTML5
- CSS3
- Bootstrap
- JavaScript

---

# Documentação Oficial

Durante o desenvolvimento do projeto foi utilizada como principal referência a documentação oficial do framework Django, conforme as boas práticas recomendadas para implementação das funcionalidades.

**Documentação utilizada**

https://docs.djangoproject.com/en/6.0/

---

# Arquitetura do Projeto

O projeto foi organizado em aplicações Django independentes, favorecendo a modularização e a manutenção do código.

```text
NUTTRIUM/

├── alimentacao/
├── perfil/
├── refeicoes/
├── core/
├── manage.py
├── db.sqlite3
└── README.md
```

---

# Como executar o projeto

## Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

Entrar na pasta

```bash
cd Nuttrium
```

---

## Criar ambiente virtual

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Executar migrações

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Executar o servidor

```bash
python manage.py runserver
```

Depois acesse

```text
http://127.0.0.1:8000/
```

---

# Fundamentação

O desenvolvimento do sistema fundamenta-se na promoção da alimentação saudável entre estudantes, considerando que a rotina escolar frequentemente dificulta o planejamento alimentar e favorece o consumo de alimentos ultraprocessados.

Ao permitir o monitoramento diário da alimentação, o Nuttrium busca incentivar escolhas alimentares mais conscientes e contribuir para o bem-estar e o desempenho acadêmico dos usuários.

---

# Equipe

**Orientador**

- Prof. Reinaldo Monteiro Cotrim

**Equipe do Projeto**

- Álvaro Guedes
- Anna Lívia Magalhães
- Ellis Carvalho Xavier

---

# Desenvolvimento do Software

Embora o projeto tenha sido desenvolvido em equipe no contexto acadêmico, todo o desenvolvimento do software, incluindo análise, modelagem, implementação do sistema, interface e integração entre os módulos, foi realizado por:

**Ellis Carvalho Xavier**

---

# 📄 Licença

Projeto desenvolvido para fins acadêmicos como parte das atividades do curso Técnico em Informática para Internet.
