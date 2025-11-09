# GreenWay

GreenWay é um aplicativo desenvolvido com **BeeWare (Toga Framework)** em **Python**, voltado para incentivar práticas sustentáveis e o descarte correto de resíduos.  
O projeto possui sistema de **login, cadastro e pontuação** com base nas ações do usuário.

## Dependências

- **Python 3.11** (Essencial ser está versão pois beeware/toga não aceitam novas versões de python ainda)
- **BeeWare / Toga**

## Como Executar o Projeto
- briefcase dev
ou gere um executável
- briefcase build
- briefcase run

### 1. Estrutura do projeto
GreenWay/
│
├── src/
│   └── GreenWay/
│       ├── app.py
│       ├── br/com/unip/aps/greenway/
│       │   ├── View/
│       │   │   ├── login.py
│       │   │   ├── register.py
│       │   │   └── home.py
│       │   └── Repository/
│       │       └── greenWayRepository.py
│       └── resources/
│           ├── images/
│           └── dataBase/greenway.db
│
└── README.md
